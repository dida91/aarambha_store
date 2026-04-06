from django.contrib import admin

from shipping.models import ShippingSettings


@admin.register(ShippingSettings)
class ShippingSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_active",
        "inside_valley_fee",
        "outside_valley_fee",
        "free_inside_valley",
        "free_delivery_all_nepal",
        "created_at",
    )
    list_filter = ("is_active", "free_inside_valley", "free_delivery_all_nepal")
