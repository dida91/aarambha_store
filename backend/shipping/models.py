from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from common.models import TimestampedModel


class ShippingConfig(TimestampedModel):
    class Zone(models.TextChoices):
        INSIDE_VALLEY = "INSIDE_VALLEY", "Inside Valley"
        OUTSIDE_VALLEY = "OUTSIDE_VALLEY", "Outside Valley"

    name = models.CharField(max_length=80, default="Default Aarambha Store Shipping")
    is_active = models.BooleanField(default=True)
    inside_valley_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
    )
    outside_valley_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
    )
    free_inside_valley = models.BooleanField(default=False)
    free_delivery_all_nepal = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="shipping_single_active_config",
            )
        ]
        indexes = [models.Index(fields=["is_active"])]

    def calculate_delivery_fee(self, zone: str):
        if self.free_delivery_all_nepal:
            return Decimal("0.00")
        if zone == self.Zone.INSIDE_VALLEY:
            if self.free_inside_valley:
                return Decimal("0.00")
            return self.inside_valley_fee
        return self.outside_valley_fee

    def __str__(self):
        return self.name
