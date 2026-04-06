from rest_framework import serializers

from promotions.models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            "id",
            "code",
            "description",
            "discount_amount",
            "min_cart_value",
            "start_at",
            "end_at",
            "usage_limit",
            "per_user_limit",
            "is_public",
            "allowed_users",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
