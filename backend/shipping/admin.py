from django.contrib import admin

from shipping.models import ShippingConfig


@admin.register(ShippingConfig)
class ShippingConfigAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_active",
        "inside_valley_fee",
        "outside_valley_fee",
        "free_inside_valley",
        "free_delivery_all_nepal",
        "created_at",
    )
    list_filter = ("is_active", "free_inside_valley", "free_delivery_all_nepal")
    search_fields = ("name",)
