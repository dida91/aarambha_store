from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from promotions.models import PromoCode, PromoUsage
from promotions.services import validate_and_calculate_discount

User = get_user_model()


@pytest.mark.django_db
def test_validate_promo_min_cart_value_rejected():
    user = User.objects.create_user(username="c1", password="pass123456")
    promo = PromoCode.objects.create(
        code="SAVE10",
        discount_type=PromoCode.DiscountType.PERCENT,
        discount_value=Decimal("10.00"),
        min_cart_value=Decimal("1000.00"),
        is_public=True,
        is_active=True,
    )
    assert promo.code == "SAVE10"
    with pytest.raises(ValidationError):
        validate_and_calculate_discount(
            user=user,
            code="SAVE10",
            subtotal=Decimal("100.00"),
        )


@pytest.mark.django_db
def test_validate_promo_per_user_limit_rejected():
    user = User.objects.create_user(username="c2", password="pass123456")
    promo = PromoCode.objects.create(
        code="ONEUSE",
        discount_type=PromoCode.DiscountType.FIXED,
        discount_value=Decimal("100.00"),
        min_cart_value=Decimal("0.00"),
        per_user_limit=1,
        is_public=True,
        is_active=True,
        starts_at=timezone.now() - timezone.timedelta(days=1),
        ends_at=timezone.now() + timezone.timedelta(days=1),
    )
    PromoUsage.objects.create(promo=promo, user=user)
    with pytest.raises(ValidationError):
        validate_and_calculate_discount(
            user=user,
            code="ONEUSE",
            subtotal=Decimal("2000.00"),
        )
