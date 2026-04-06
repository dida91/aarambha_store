from django.db import models
from django.db.models import Q

from common.models import TimestampedModel


class ShippingSettings(TimestampedModel):
    is_active = models.BooleanField(default=True)
    inside_valley_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outside_valley_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    free_inside_valley = models.BooleanField(default=False)
    free_delivery_all_nepal = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="shipping_single_active_settings",
            )
        ]

    def __str__(self):
        return f"ShippingSettings({self.id})"
