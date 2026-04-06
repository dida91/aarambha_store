from decimal import Decimal

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from promotions.models import PromoCode, PromoUsage


def validate_and_calculate_discount(*, user, code: str | None, subtotal: Decimal):
    if not code:
        return Decimal("0"), None

    now = timezone.now()
    try:
        promo = PromoCode.objects.prefetch_related("allowed_users").get(
            code__iexact=code
        )
    except PromoCode.DoesNotExist as exc:
        raise ValidationError({"promo_code": ["Invalid promo code."]}) from exc

    if not promo.is_active:
        raise ValidationError({"promo_code": ["Promo code is inactive."]})
    if promo.starts_at and promo.starts_at > now:
        raise ValidationError({"promo_code": ["Promo code is not active yet."]})
    if promo.ends_at and promo.ends_at < now:
        raise ValidationError({"promo_code": ["Promo code has expired."]})
    if subtotal < promo.min_cart_value:
        raise ValidationError(
            {"promo_code": ["Minimum cart value not met for this promo."]}
        )

    if promo.usage_limit is not None and promo.used_count >= promo.usage_limit:
        raise ValidationError({"promo_code": ["Promo usage limit reached."]})

    if not promo.is_public and not promo.allowed_users.filter(id=user.id).exists():
        raise ValidationError({"promo_code": ["You are not eligible for this promo."]})

    if promo.per_user_limit is not None:
        user_uses = PromoUsage.objects.filter(promo=promo, user=user).count()
        if user_uses >= promo.per_user_limit:
            raise ValidationError(
                {"promo_code": ["Per-user promo usage limit reached."]}
            )

    if promo.discount_type == PromoCode.DiscountType.PERCENT:
        discount = (subtotal * promo.discount_value) / Decimal("100")
    else:
        discount = promo.discount_value

    if discount > subtotal:
        discount = subtotal

    return discount.quantize(Decimal("0.01")), promo
