from django.contrib import admin

from promotions.models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_type",
        "discount_value",
        "min_cart_value",
        "is_public",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = ("discount_type", "is_public", "is_active")
    search_fields = ("code",)
    filter_horizontal = ("allowed_users",)
