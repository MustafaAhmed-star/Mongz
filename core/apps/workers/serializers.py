from rest_framework import serializers
from apps.users.serializers import UserSerializer
from .models import ServiceCategory, WorkerProfile


MAX_IMAGE_SIZE = 5 * 1024 * 1024


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "image"]

    def validate_image(self, value):
        if value and value.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError("Image size must not exceed 5 MB.")
        return value


class WorkerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    score = serializers.SerializerMethodField()

    class Meta:
        model = WorkerProfile
        fields = [
            "id", "user", "category", "experience_years",
            "average_rating", "completed_jobs", "is_available",
            "score", "created_at",
        ]
        read_only_fields = ["average_rating", "completed_jobs", "created_at"]

    def get_score(self, obj):
        return round(obj.calculate_score(), 2)


class WorkerProfileWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source="category",
    )

    class Meta:
        model = WorkerProfile
        fields = ["category_id", "experience_years", "is_available"]

    def validate(self, attrs):
        user = self.context["request"].user
        if self.instance is None and hasattr(user, "worker_profile"):
            raise serializers.ValidationError("You already have a worker profile.")
        return attrs

    def create(self, validated_data):
        return WorkerProfile.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )
