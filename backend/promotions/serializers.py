from rest_framework import serializers

from promotions.models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "min_cart_value",
            "starts_at",
            "ends_at",
            "usage_limit",
            "per_user_limit",
            "used_count",
            "is_public",
            "is_active",
            "allowed_users",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        starts_at = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends_at = attrs.get("ends_at", getattr(self.instance, "ends_at", None))
        if starts_at and ends_at and starts_at > ends_at:
            raise serializers.ValidationError("starts_at cannot be after ends_at.")
        return attrs
