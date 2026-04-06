from django.contrib import admin

from promotions.models import PromoCode, PromoUsage


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_type",
        "discount_value",
        "min_cart_value",
        "usage_limit",
        "per_user_limit",
        "used_count",
        "is_public",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = ("discount_type", "is_public", "is_active")
    search_fields = ("code",)
    filter_horizontal = ("allowed_users",)


@admin.register(PromoUsage)
class PromoUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "promo", "user", "order", "created_at")
    search_fields = ("promo__code", "user__username", "order__id")
