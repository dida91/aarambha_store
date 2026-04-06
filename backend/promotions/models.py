from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from common.models import TimestampedModel


class PromoCode(TimestampedModel):
    class DiscountType(models.TextChoices):
        PERCENT = "PERCENT", "Percent"
        FIXED = "FIXED", "Fixed"

    code = models.CharField(max_length=40, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    per_user_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="promo_codes"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["is_active"])]

    def __str__(self):
        return self.code


class PromoUsage(TimestampedModel):
    promo = models.ForeignKey(
        PromoCode, on_delete=models.CASCADE, related_name="usages"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="promo_usages"
    )
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="promo_usage",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["promo", "user", "order"],
                name="unique_promo_usage_user_order",
            )
        ]

    def __str__(self):
        return f"{self.promo.code} by {self.user_id}"
