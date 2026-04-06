from decimal import Decimal

from rest_framework import serializers

from cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=12, decimal_places=2, read_only=True
    )
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "line_total",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "updated_at",
            "product_name",
            "product_price",
            "line_total",
        ]

    def get_line_total(self, obj):
        return obj.product.price * Decimal(obj.quantity)

    def validate(self, attrs):
        product = attrs.get("product") or self.instance.product
        quantity = attrs.get("quantity", self.instance.quantity if self.instance else 1)
        if quantity > product.stock:
            raise serializers.ValidationError(
                {"quantity": "Requested quantity exceeds stock."}
            )
        if not product.is_active:
            raise serializers.ValidationError({"product": "Product is not active."})
        return attrs
