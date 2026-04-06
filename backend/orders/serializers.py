from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from cart.models import CartItem
from orders.models import Order, OrderItem, OrderStatusHistory
from promotions.models import PromoCode, PromoUsage
from shipping.models import ShippingAddress, ShippingConfig


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name_snapshot",
            "product_sku_snapshot",
            "unit_price_snapshot",
            "quantity",
            "line_total",
        ]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = [
            "id",
            "from_status",
            "to_status",
            "actor",
            "actor_username",
            "note",
            "created_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "subtotal",
            "promo_discount",
            "shipping_fee",
            "total_amount",
            "promo_code_snapshot",
            "shipping_snapshot",
            "rejection_reason",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        ]


class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    promo_code = serializers.CharField(required=False, allow_blank=True)

    @transaction.atomic
    def create_order(self, user):
        cart_items = (
            CartItem.objects.select_related("product")
            .select_for_update()
            .filter(user=user)
            .order_by("id")
        )
        if not cart_items.exists():
            raise serializers.ValidationError({"cart": "Cart is empty."})

        shipping_address = ShippingAddress.objects.filter(
            user=user, id=self.validated_data["shipping_address_id"]
        ).first()
        if not shipping_address:
            raise serializers.ValidationError(
                {"shipping_address_id": "Shipping address not found."}
            )

        shipping_config = ShippingConfig.objects.filter(is_active=True).first()
        if not shipping_config:
            raise serializers.ValidationError(
                {"shipping_config": "No active shipping config."}
            )

        subtotal = Decimal("0.00")
        line_items = []

        for item in cart_items:
            product = item.product
            if not product.is_active:
                raise serializers.ValidationError(
                    {"product": f"{product.name} is not active."}
                )
            if product.stock < item.quantity:
                raise serializers.ValidationError(
                    {"stock": f"Insufficient stock for {product.name}."}
                )

            line_total = product.price * Decimal(item.quantity)
            subtotal += line_total
            line_items.append((item, product, line_total))

        promo_discount = Decimal("0.00")
        promo_obj = None
        promo_code = self.validated_data.get("promo_code", "").strip()
        if promo_code:
            promo_obj = (
                PromoCode.objects.select_for_update()
                .filter(code__iexact=promo_code)
                .first()
            )
            if not promo_obj:
                raise serializers.ValidationError(
                    {"promo_code": "Promo code not found."}
                )
            is_valid, message = promo_obj.is_valid_for(user, subtotal)
            if not is_valid:
                raise serializers.ValidationError({"promo_code": message})
            promo_discount = min(subtotal, promo_obj.discount_amount)

        shipping_fee = shipping_config.calculate_fee(shipping_address.area, subtotal)
        total_amount = subtotal - promo_discount + shipping_fee

        order = Order.objects.create(
            user=user,
            status=Order.Status.PENDING,
            subtotal=subtotal,
            promo_discount=promo_discount,
            shipping_fee=shipping_fee,
            total_amount=total_amount,
            promo_code_snapshot=promo_obj.code if promo_obj else "",
            shipping_snapshot={
                "name": shipping_address.full_name,
                "phone": shipping_address.phone,
                "area": shipping_address.area,
                "district": shipping_address.district,
                "city": shipping_address.city,
                "address_line": shipping_address.address_line,
                "landmark": shipping_address.landmark,
                "inside_valley_charge": str(shipping_config.inside_valley_charge),
                "outside_valley_charge": str(shipping_config.outside_valley_charge),
                "free_inside_valley": shipping_config.free_inside_valley,
                "free_delivery_all_nepal": shipping_config.free_delivery_all_nepal,
            },
        )

        for cart_item, product, line_total in line_items:
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name_snapshot=product.name,
                product_sku_snapshot=product.sku,
                unit_price_snapshot=product.price,
                quantity=cart_item.quantity,
                line_total=line_total,
            )
            product.stock = F("stock") - cart_item.quantity
            product.save(update_fields=["stock"])

        if promo_obj:
            PromoUsage.objects.create(promo=promo_obj, user=user, order=order)

        OrderStatusHistory.objects.create(
            order=order,
            from_status="",
            to_status=Order.Status.PENDING,
            actor=user,
            note="Order created through checkout.",
        )

        cart_items.delete()
        order.refresh_from_db()
        return order


class SellerOrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[Order.Status.CONFIRMED, Order.Status.REJECTED]
    )
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    note = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        order = self.context["order"]
        if order.status != Order.Status.PENDING:
            raise serializers.ValidationError(
                "Only PENDING orders can be transitioned."
            )
        if (
            attrs["status"] == Order.Status.REJECTED
            and not attrs.get("rejection_reason", "").strip()
        ):
            raise serializers.ValidationError(
                {
                    "rejection_reason": "Rejection reason is required for rejected orders."
                }
            )
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        order = self.context["order"]
        actor = self.context["request"].user
        previous_status = order.status

        order.status = self.validated_data["status"]
        if order.status == Order.Status.REJECTED:
            order.rejection_reason = self.validated_data.get("rejection_reason", "")
        order.save(update_fields=["status", "rejection_reason", "updated_at"])

        OrderStatusHistory.objects.create(
            order=order,
            from_status=previous_status,
            to_status=order.status,
            actor=actor,
            note=self.validated_data.get("note", ""),
        )
        return order
