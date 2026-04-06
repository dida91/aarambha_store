from rest_framework import serializers

from shipping.models import ShippingAddress, ShippingConfig


class ShippingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingConfig
        fields = [
            "id",
            "name",
            "inside_valley_charge",
            "outside_valley_charge",
            "free_inside_valley",
            "free_delivery_all_nepal",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "full_name",
            "phone",
            "area",
            "district",
            "city",
            "address_line",
            "landmark",
            "is_default",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        if validated_data.get("is_default"):
            ShippingAddress.objects.filter(user=user, is_default=True).update(
                is_default=False
            )
        return ShippingAddress.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("is_default"):
            ShippingAddress.objects.filter(user=instance.user, is_default=True).exclude(
                pk=instance.pk
            ).update(is_default=False)
        return super().update(instance, validated_data)
