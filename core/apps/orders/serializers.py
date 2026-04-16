from rest_framework import serializers
from apps.users.serializers import UserSerializer
from apps.workers.serializers import ServiceCategorySerializer
from apps.workers.models import ServiceCategory
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    
    client = UserSerializer(read_only=True)
    worker = UserSerializer(read_only=True)
    service_category = ServiceCategorySerializer(read_only=True)

    # Show payment info nested inside the order response
    commission_payment = serializers.SerializerMethodField()

    class Meta:
        model  = Order
        fields = [
            "id",
            "client",
            "worker",
            "service_category",
            "price",
            "commission",
            "status",
            "created_at",
            "accepted_at",
            "completed_at",
            "cancelled_at",
            "commission_payment",
        ]

    def get_commission_payment(self, order):
        """
        Return payment info if it exists, None if it doesn't.
        We never expose payment_key — it's sensitive.
        """
        try:
            p = order.commission_payment
            return {
                "amount": str(p.amount),
                "payment_status": p.payment_status,
                "paymob_order_id": p.paymob_order_id,
                "paymob_transaction_id": p.paymob_transaction_id,
            }
        except Exception:
            return None


class OrderCreateSerializer(serializers.ModelSerializer):
    
    service_category = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all()
    )

    class Meta:
        model  = Order
        fields = ["service_category", "price"]
