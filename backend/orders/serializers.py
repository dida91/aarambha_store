from rest_framework import serializers

from orders.models import Order, OrderItem, OrderStatusHistory
from shipping.models import ShippingConfig


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ["id", "status", "actor", "actor_username", "note", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "unit_price",
            "quantity",
            "line_total",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    timeline = OrderStatusHistorySerializer(
        source="status_history", many=True, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "subtotal",
            "discount_total",
            "shipping_fee",
            "grand_total",
            "rejection_reason",
            "shipping_snapshot",
            "items",
            "timeline",
            "created_at",
            "updated_at",
        ]


class CheckoutSerializer(serializers.Serializer):
    zone = serializers.ChoiceField(choices=ShippingConfig.Zone.choices)
    promo_code = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(max_length=250)
    city = serializers.CharField(max_length=80)
    contact_phone = serializers.CharField(max_length=20)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    note = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
