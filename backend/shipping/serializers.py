from rest_framework import serializers

from shipping.models import ShippingConfig


class ShippingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingConfig
        fields = [
            "id",
            "name",
            "is_active",
            "inside_valley_fee",
            "outside_valley_fee",
            "free_inside_valley",
            "free_delivery_all_nepal",
            "created_at",
            "updated_at",
        ]
