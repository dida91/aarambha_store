from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from cart.models import CartItem
from catalog.models import Product
from orders.models import Order
from promotions.models import PromoCode
from shipping.models import ShippingAddress, ShippingConfig

User = get_user_model()


@pytest.mark.django_db
def test_checkout_creates_order_and_decrements_stock():
    user = User.objects.create_user(
        username="cust", email="cust@example.com", password="StrongPass123"
    )
    seller = User.objects.create_user(
        username="seller",
        email="seller@example.com",
        password="StrongPass123",
        role="SELLER",
    )
    assert seller.role == "SELLER"

    product = Product.objects.create(
        name="Tea",
        slug="tea",
        sku="SKU-TEA-1",
        price=Decimal("100.00"),
        stock=5,
        is_active=True,
    )
    CartItem.objects.create(user=user, product=product, quantity=2)

    ShippingConfig.objects.create(
        name="Default",
        inside_valley_charge=Decimal("50.00"),
        outside_valley_charge=Decimal("100.00"),
        free_inside_valley=False,
        free_delivery_all_nepal=False,
        is_active=True,
    )

    address = ShippingAddress.objects.create(
        user=user,
        full_name="Customer",
        phone="9800000000",
        area="INSIDE_VALLEY",
        district="Kathmandu",
        city="Kathmandu",
        address_line="Baneshwor",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(
        "/api/orders/checkout/", {"shipping_address_id": address.id}, format="json"
    )
    assert response.status_code == 201
    assert response.data["success"] is True

    order = Order.objects.get(id=response.data["data"]["id"])
    assert order.status == Order.Status.PENDING
    assert order.subtotal == Decimal("200.00")
    assert order.shipping_fee == Decimal("50.00")
    assert order.total_amount == Decimal("250.00")

    product.refresh_from_db()
    assert product.stock == 3


@pytest.mark.django_db
def test_checkout_applies_valid_promo_and_limits():
    user = User.objects.create_user(
        username="promo", email="promo@example.com", password="StrongPass123"
    )
    product = Product.objects.create(
        name="Mug",
        slug="mug",
        sku="SKU-MUG-1",
        price=Decimal("500.00"),
        stock=10,
        is_active=True,
    )
    CartItem.objects.create(user=user, product=product, quantity=1)

    ShippingConfig.objects.create(
        name="Default",
        inside_valley_charge=Decimal("30.00"),
        outside_valley_charge=Decimal("80.00"),
        free_inside_valley=True,
        free_delivery_all_nepal=False,
        is_active=True,
    )

    address = ShippingAddress.objects.create(
        user=user,
        full_name="Promo User",
        phone="9800000001",
        area="INSIDE_VALLEY",
        district="Kathmandu",
        city="Kathmandu",
        address_line="Boudha",
    )

    from datetime import timedelta

    from django.utils import timezone

    PromoCode.objects.create(
        code="NEW500",
        discount_amount=Decimal("100.00"),
        min_cart_value=Decimal("400.00"),
        start_at=timezone.now() - timedelta(days=1),
        end_at=timezone.now() + timedelta(days=1),
        usage_limit=5,
        per_user_limit=1,
        is_public=True,
        is_active=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        "/api/orders/checkout/",
        {"shipping_address_id": address.id, "promo_code": "NEW500"},
        format="json",
    )

    assert response.status_code == 201
    assert Decimal(response.data["data"]["promo_discount"]) == Decimal("100.00")
    assert Decimal(response.data["data"]["shipping_fee"]) == Decimal("0.00")
    assert Decimal(response.data["data"]["total_amount"]) == Decimal("400.00")


@pytest.mark.django_db
def test_order_status_transition_requires_rejection_reason_and_no_invalid_jump():
    seller = User.objects.create_user(
        username="s1", email="s1@example.com", password="StrongPass123", role="SELLER"
    )
    user = User.objects.create_user(
        username="c1", email="c1@example.com", password="StrongPass123"
    )

    order = Order.objects.create(
        user=user,
        status=Order.Status.PENDING,
        subtotal=Decimal("100.00"),
        promo_discount=Decimal("0.00"),
        shipping_fee=Decimal("10.00"),
        total_amount=Decimal("110.00"),
        shipping_snapshot={},
    )

    client = APIClient()
    client.force_authenticate(user=seller)

    bad = client.post(
        f"/api/orders/seller/{order.id}/status/", {"status": "REJECTED"}, format="json"
    )
    assert bad.status_code == 400

    ok = client.post(
        f"/api/orders/seller/{order.id}/status/",
        {
            "status": "REJECTED",
            "rejection_reason": "Out of stock",
            "note": "manual reject",
        },
        format="json",
    )
    assert ok.status_code == 200

    again = client.post(
        f"/api/orders/seller/{order.id}/status/", {"status": "CONFIRMED"}, format="json"
    )
    assert again.status_code == 400
