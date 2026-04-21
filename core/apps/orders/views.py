import logging
from datetime import datetime, timezone

from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification
from apps.payments.models import CommissionPayment
from apps.payments import paymob
from apps.users.models import User
from apps.workers.models import WorkerProfile
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer

logger = logging.getLogger(__name__)

#Helper funcs

def now():
    return datetime.now(tz=timezone.utc)


def send_notification(user, title, message, notif_type=Notification.IN_APP):
    Notification.objects.create(
        user=user, title=title, message=message, type=notif_type,
    )


def authorize_commission(order):
    amount = settings.COMMISSION_AMOUNT

    try:
        paymob_order_id, payment_key = paymob.authorize_commission(order)
        CommissionPayment.objects.create(
            order=order,
            amount=amount,
            paymob_order_id=paymob_order_id,
            payment_key=payment_key,
            payment_status=CommissionPayment.AUTHORIZED,
        )
        logger.info(f"Commission AUTHORIZED — Order #{order.id}")
        return payment_key

    except Exception as e:
        logger.error(f"Paymob authorization FAILED for Order #{order.id}: {e}")
        CommissionPayment.objects.create(
            order=order,
            amount=amount,
            payment_status=CommissionPayment.FAILED,
        )
        return None

#orders views
class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == User.Role.CLIENT:
            orders = Order.objects.filter(client=user)
        elif user.role == User.Role.WORKER:
            orders = Order.objects.filter(worker=user)
        else:
            orders = Order.objects.all()
        return Response(OrderSerializer(orders, many=True).data)

    @transaction.atomic
    def post(self, request):
        if request.user.role != User.Role.CLIENT:
            return Response(
                {"error": "Only clients can create orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            client=request.user,
            service_category=serializer.validated_data["service_category"],
            worker=serializer.validated_data.get("worker"),
        )

        payment_key = authorize_commission(order)

        available_workers = WorkerProfile.objects.select_related("user").filter(
            user__role=User.Role.WORKER,
            is_available=True,
            profession__iexact=order.service_category.name,
        )

        for wp in available_workers:
            if order.worker and order.worker == wp.user:
                title = "You Were Selected For an Order 🎯"
                message = (
                    f"A client chose you for a {order.service_category.name} "
                    f"order #{order.id}. Please accept or reject."
                )
            else:
                title = "New Order Available"
                message = f"New {order.service_category.name} order #{order.id} is available."

            send_notification(wp.user, title=title, message=message, notif_type=Notification.PUSH)

        response_data = OrderSerializer(order).data
        response_data["payment_key"] = payment_key
        return Response(response_data, status=status.HTTP_201_CREATED)