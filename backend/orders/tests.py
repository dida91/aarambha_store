from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from cart.models import Cart, CartItem
from catalog.models import Category, Product
from orders.models import Order
from orders.services import create_order_from_cart, update_order_status
from shipping.models import ShippingConfig

User = get_user_model()


@pytest.mark.django_db
def test_checkout_creates_order_and_reduces_stock():
    customer = User.objects.create_user(
        username="buyer1",
        password="pass123456",
        role=User.Role.CUSTOMER,
    )
    category = Category.objects.create(name="Tea", slug="tea")
    product = Product.objects.create(
        category=category,
        name="Ilam Tea",
        slug="ilam-tea",
        price=Decimal("500.00"),
        stock_quantity=10,
        is_active=True,
    )
    cart = Cart.objects.create(user=customer)
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    ShippingConfig.objects.create(
        name="Default",
        is_active=True,
        inside_valley_fee=Decimal("100.00"),
        outside_valley_fee=Decimal("200.00"),
    )

    order = create_order_from_cart(
        user=customer,
        zone=ShippingConfig.Zone.INSIDE_VALLEY,
        address="Lalitpur",
        city="Kathmandu",
        contact_phone="9800000000",
        promo_code="",
    )

    assert order.status == Order.Status.PENDING
    assert order.subtotal == Decimal("1000.00")
    assert order.shipping_fee == Decimal("100.00")
    assert order.grand_total == Decimal("1100.00")

    product.refresh_from_db()
    assert product.stock_quantity == 8
    assert CartItem.objects.filter(cart=cart).count() == 0


@pytest.mark.django_db
def test_checkout_prevents_overselling_with_select_for_update_flow():
    customer = User.objects.create_user(
        username="buyer2",
        password="pass123456",
        role=User.Role.CUSTOMER,
    )
    category = Category.objects.create(name="Coffee", slug="coffee")
    product = Product.objects.create(
        category=category,
        name="Nepal Coffee",
        slug="nepal-coffee",
        price=Decimal("300.00"),
        stock_quantity=1,
        is_active=True,
    )
    cart = Cart.objects.create(user=customer)
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    ShippingConfig.objects.create(
        name="Default",
        is_active=True,
        inside_valley_fee=Decimal("50.00"),
        outside_valley_fee=Decimal("100.00"),
    )

    with pytest.raises(ValidationError):
        create_order_from_cart(
            user=customer,
            zone=ShippingConfig.Zone.INSIDE_VALLEY,
            address="Bhaktapur",
            city="Bhaktapur",
            contact_phone="9800000001",
            promo_code="",
        )


@pytest.mark.django_db
def test_order_status_transition_validation_rejects_invalid_jump():
    seller = User.objects.create_user(
        username="seller1",
        password="pass123456",
        role=User.Role.SELLER,
    )
    customer = User.objects.create_user(
        username="buyer3",
        password="pass123456",
        role=User.Role.CUSTOMER,
    )
    order = Order.objects.create(
        user=customer,
        status=Order.Status.PENDING,
        subtotal=Decimal("100.00"),
        discount_total=Decimal("0.00"),
        shipping_fee=Decimal("10.00"),
        grand_total=Decimal("110.00"),
        shipping_snapshot={"zone": "INSIDE_VALLEY"},
    )

    update_order_status(
        order=order,
        actor=seller,
        status=Order.Status.CONFIRMED,
        note="Confirmed",
        rejection_reason="",
    )

    with pytest.raises(ValidationError):
        update_order_status(
            order=order,
            actor=seller,
            status=Order.Status.REJECTED,
            note="Invalid jump",
            rejection_reason="Out of stock",
        )
