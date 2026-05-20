from django.contrib import admin
from .models import ServiceCategory, WorkerProfile


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image"]
    search_fields = ["name"]


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "experience_years",
                    "average_rating", "completed_jobs", "is_available"]
    list_filter = ["category", "is_available"]
    search_fields = ["user__username", "category__name"]
    readonly_fields = ["average_rating", "completed_jobs", "created_at"]
