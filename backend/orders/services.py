from decimal import Decimal

from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem, OrderStatusHistory
from promotions.models import PromoUsage
from promotions.services import validate_and_calculate_discount
from shipping.services import get_active_shipping_config


@transaction.atomic
def create_order_from_cart(
    *,
    user,
    zone: str,
    address: str,
    city: str,
    contact_phone: str,
    promo_code: str | None,
):
    cart = Cart.objects.select_for_update().get(user=user)
    cart_items = list(
        CartItem.objects.select_for_update()
        .select_related("product")
        .filter(cart=cart)
        .order_by("id")
    )
    if not cart_items:
        raise ValidationError({"cart": ["Cart is empty."]})

    subtotal = Decimal("0.00")
    for item in cart_items:
        if item.product.stock_quantity < item.quantity:
            raise ValidationError(
                {"stock": [f"Insufficient stock for '{item.product.name}'."]}
            )
        subtotal += item.product.price * item.quantity

    discount_total, promo = validate_and_calculate_discount(
        user=user,
        code=promo_code,
        subtotal=subtotal,
    )

    shipping_config = get_active_shipping_config()
    shipping_fee = shipping_config.calculate_delivery_fee(zone)
    grand_total = (subtotal - discount_total) + shipping_fee

    shipping_snapshot = {
        "zone": zone,
        "address": address,
        "city": city,
        "contact_phone": contact_phone,
        "config_id": shipping_config.id,
        "inside_valley_fee": str(shipping_config.inside_valley_fee),
        "outside_valley_fee": str(shipping_config.outside_valley_fee),
        "free_inside_valley": shipping_config.free_inside_valley,
        "free_delivery_all_nepal": shipping_config.free_delivery_all_nepal,
        "applied_shipping_fee": str(shipping_fee),
    }

    order = Order.objects.create(
        user=user,
        status=Order.Status.PENDING,
        subtotal=subtotal,
        discount_total=discount_total,
        shipping_fee=shipping_fee,
        grand_total=grand_total,
        shipping_snapshot=shipping_snapshot,
    )

    order_items = []
    for item in cart_items:
        line_total = item.product.price * item.quantity
        order_items.append(
            OrderItem(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_slug=item.product.slug,
                unit_price=item.product.price,
                quantity=item.quantity,
                line_total=line_total,
            )
        )
        item.product.stock_quantity = F("stock_quantity") - item.quantity
        item.product.save(update_fields=["stock_quantity"])

    OrderItem.objects.bulk_create(order_items)

    OrderStatusHistory.objects.create(
        order=order,
        status=Order.Status.PENDING,
        actor=user,
        note="Order created from cart checkout.",
    )

    if promo:
        promo.used_count = F("used_count") + 1
        promo.save(update_fields=["used_count"])
        PromoUsage.objects.create(promo=promo, user=user, order=order)

    CartItem.objects.filter(cart=cart).delete()
    return order


@transaction.atomic
def update_order_status(
    *, order: Order, actor, status: str, note: str, rejection_reason: str
):
    if status == order.status:
        raise ValidationError({"status": ["Order is already in requested status."]})

    if not order.can_transition_to(status):
        raise ValidationError(
            {"status": [f"Invalid status transition from {order.status} to {status}."]}
        )

    if status == Order.Status.REJECTED and not rejection_reason:
        raise ValidationError({"rejection_reason": ["Rejection reason is required."]})

    order.status = status
    if status == Order.Status.REJECTED:
        order.rejection_reason = rejection_reason
    else:
        order.rejection_reason = None
    order.save(update_fields=["status", "rejection_reason", "updated_at"])

    OrderStatusHistory.objects.create(
        order=order,
        status=status,
        actor=actor,
        note=note or "",
    )

    return order
