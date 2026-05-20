from rest_framework import serializers
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.workers.models import ServiceCategory, WorkerProfile
from apps.workers.serializers import ServiceCategorySerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    client = UserSerializer(read_only=True)
    worker = UserSerializer(read_only=True)
    service_category = ServiceCategorySerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "client",
            "worker",
            "service_category",
            "description",
            "address",
            "phone",
            "status",
            "created_at",
            "accepted_at",
            "started_at",
            "completed_at",
            "rejected_at",
            "cancelled_at",
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )
    address = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=255,
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        trim_whitespace=True,
        max_length=20,
    )

    service_category = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
    )
    # worker_id is REQUIRED — the client must choose a specific worker (direct assignment)
    worker_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role=User.Role.WORKER),
        source="worker",
        required=True,
    )

    class Meta:
        model = Order
        fields = ["service_category", "worker_id", "description", "address", "phone"]

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Order description is required.")
        return value.strip()

    def validate(self, attrs):
        """
        Validate that the chosen worker:
          1. Has a profile
          2. Is currently available
          3. Belongs to the selected service category
        """
        worker = attrs["worker"]
        service_category = attrs["service_category"]

        if not hasattr(worker, "worker_profile"):
            raise serializers.ValidationError(
                {"worker_id": "This worker does not have a profile yet."}
            )

        profile = worker.worker_profile

        if not profile.is_available:
            raise serializers.ValidationError(
                {"worker_id": "This worker is not currently available."}
            )

        if profile.category_id != service_category.id:
            raise serializers.ValidationError(
                {
                    "worker_id": (
                        "This worker does not belong to the selected category."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        client = request.user

        address = validated_data.get("address", "")
        phone = validated_data.get("phone", "")

        return Order.objects.create(
            client=client,
            service_category=validated_data["service_category"],
            worker=validated_data["worker"],
            description=validated_data["description"],
            address=address.strip() or client.address,
            phone=phone.strip() or client.phone,
        )
