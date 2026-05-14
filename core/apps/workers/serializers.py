from rest_framework import serializers
from core.apps.users.serializers import UserSerializer
from .models import ServiceCategory, WorkerProfile


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name"]


class WorkerProfileSerializer(serializers.ModelSerializer):
  
    user = UserSerializer(read_only=True)
    service_category = ServiceCategorySerializer(read_only=True)
    score = serializers.SerializerMethodField()

    class Meta:
        model  = WorkerProfile
        fields = [
            "id", "user", "profession", "experience_years",
            "service_category",
            "average_rating", "completed_jobs", "is_available",
            "score", "created_at",
        ]
        read_only_fields = ["average_rating", "completed_jobs", "created_at"]

    def get_score(self, obj):
        return round(getattr(obj, "score", obj.calculate_score()), 2)


class WorkerProfileWriteSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = WorkerProfile
        fields = ["profession", "service_category", "experience_years", "is_available"]
        extra_kwargs = {"profession": {"required": False}}

    def validate(self, attrs):
        # Make sure this worker doesn't already have a profile
        user = self.context["request"].user
        if self.instance is None and hasattr(user, "worker_profile"):
            raise serializers.ValidationError("You already have a worker profile.")
        if self.instance is None and not attrs.get("profession") and not attrs.get("service_category"):
            raise serializers.ValidationError("Choose a service category or enter a profession.")
        return attrs

    def create(self, validated_data):
        service_category = validated_data.get("service_category")
        if service_category and not validated_data.get("profession"):
            validated_data["profession"] = service_category.name

        return WorkerProfile.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )

    def update(self, instance, validated_data):
        service_category = validated_data.get("service_category")
        if service_category and not validated_data.get("profession"):
            validated_data["profession"] = service_category.name
        return super().update(instance, validated_data)
