from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id", "client", "worker", "service_category",
        "status", "created_at",
    ]
    list_filter = ["status", "service_category"]
    search_fields = [
        "client__username",
        "worker__username",
        "description",
        "address",
        "phone",
    ]
    readonly_fields = [
        "created_at",
        "accepted_at",
        "started_at",
        "completed_at",
        "rejected_at",
        "cancelled_at",
    ]
    date_hierarchy = "created_at"
