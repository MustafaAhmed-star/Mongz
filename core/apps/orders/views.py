from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification
from apps.users.models import User
from apps.workers.models import WorkerProfile
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


def send_notification(user, title, message, notif_type=Notification.IN_APP):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=notif_type,
    )


def validation_error_response(exc):
    if hasattr(exc, "message_dict"):
        return Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": exc.messages}, status=status.HTTP_400_BAD_REQUEST)


def get_worker_profile(user):
    try:
        return user.worker_profile
    except WorkerProfile.DoesNotExist:
        return None


def user_can_view_order(user, order):
    """
    Clients see their own orders.
    Workers see orders assigned to them.
    Admins see everything.
    """
    if user.role == User.Role.ADMIN:
        return True
    if order.client_id == user.id:
        return True
    if order.worker_id == user.id:
        return True
    return False


def serialize_order(order, request):
    return OrderSerializer(order, context={"request": request}).data


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.select_related("client", "worker", "service_category")
        if user.role == User.Role.CLIENT:
            orders = orders.filter(client=user)
        elif user.role == User.Role.WORKER:
            # Workers only see orders directly assigned to them
            orders = orders.filter(worker=user)
        else:
            # Admin sees everything
            orders = orders.all()

        serializer = OrderSerializer(
            orders,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        if request.user.role != User.Role.CLIENT:
            return Response(
                {"error": "Only clients can create orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrderCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()

        # Direct assignment — notify only the chosen worker
        send_notification(
            order.worker,
            title="You were selected for an order",
            message=(
                f"A client chose you for order #{order.id} "
                f"in {order.service_category.name}."
            ),
            notif_type=Notification.PUSH,
        )

        return Response(serialize_order(order, request), status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user_can_view_order(request.user, order):
            return Response(
                {"error": "You do not have access to this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(serialize_order(order, request))


class OrderAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can accept orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.select_for_update().select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only the specifically assigned worker can accept
        if order.worker_id != request.user.id:
            return Response(
                {"error": "This order is not assigned to you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        profile = get_worker_profile(request.user)
        if not profile:
            return Response(
                {"error": "You must create a worker profile before accepting orders."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not profile.is_available:
            return Response(
                {"error": "You are currently marked as unavailable."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order.validate_transition_to(Order.ACCEPTED)
        except DjangoValidationError as exc:
            return validation_error_response(exc)

        order.status = Order.ACCEPTED
        order.accepted_at = timezone.now()
        order.save(update_fields=["status", "accepted_at"])

        send_notification(
            order.client,
            title="Order accepted ✅",
            message=f"{request.user.username} accepted your order #{order.id}.",
            notif_type=Notification.PUSH,
        )
        return Response(serialize_order(order, request))


class OrderRejectView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can reject orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.select_for_update().select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.worker_id != request.user.id:
            return Response(
                {"error": "Only the assigned worker can reject this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order.validate_transition_to(Order.REJECTED)
        except DjangoValidationError as exc:
            return validation_error_response(exc)

        order.status = Order.REJECTED
        order.rejected_at = timezone.now()
        order.save(update_fields=["status", "rejected_at"])

        send_notification(
            order.client,
            title="Order rejected",
            message=f"Your order #{order.id} was rejected by the selected worker.",
            notif_type=Notification.PUSH,
        )
        return Response(serialize_order(order, request))


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        if request.user.role != User.Role.CLIENT:
            return Response(
                {"error": "Only clients can cancel orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.select_for_update().select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk, client=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            order.validate_transition_to(Order.CANCELLED)
        except DjangoValidationError as exc:
            return validation_error_response(exc)

        order.status = Order.CANCELLED
        order.cancelled_at = timezone.now()
        order.save(update_fields=["status", "cancelled_at"])

        send_notification(
            order.worker,
            title="Order cancelled",
            message=f"Order #{order.id} was cancelled by the client.",
            notif_type=Notification.IN_APP,
        )
        return Response(serialize_order(order, request))


class OrderStartView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can start orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.select_for_update().select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.worker_id != request.user.id:
            return Response(
                {"error": "Only the assigned worker can start this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order.validate_transition_to(Order.IN_PROGRESS)
        except DjangoValidationError as exc:
            return validation_error_response(exc)

        order.status = Order.IN_PROGRESS
        order.started_at = timezone.now()
        order.save(update_fields=["status", "started_at"])

        send_notification(
            order.client,
            title="Order in progress 🔧",
            message=f"Your order #{order.id} is now in progress.",
            notif_type=Notification.PUSH,
        )
        return Response(serialize_order(order, request))


class OrderCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        if request.user.role != User.Role.WORKER:
            return Response(
                {"error": "Only workers can complete orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = Order.objects.select_for_update().select_related(
                "client",
                "worker",
                "service_category",
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.worker_id != request.user.id:
            return Response(
                {"error": "Only the assigned worker can complete this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order.validate_transition_to(Order.COMPLETED)
        except DjangoValidationError as exc:
            return validation_error_response(exc)

        order.status = Order.COMPLETED
        order.completed_at = timezone.now()
        order.save(update_fields=["status", "completed_at"])

        profile = WorkerProfile.objects.select_for_update().get(user=request.user)
        profile.completed_jobs += 1
        profile.save(update_fields=["completed_jobs"])

        send_notification(
            order.client,
            title="Job completed ✅",
            message=f"Order #{order.id} is done. You can now rate the worker.",
            notif_type=Notification.PUSH,
        )
        return Response(serialize_order(order, request))
