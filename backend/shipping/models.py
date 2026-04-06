from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from common.constants import DELIVERY_AREAS, INSIDE_VALLEY, ZERO_DECIMAL


class ShippingConfig(models.Model):
    name = models.CharField(max_length=120, default="Default Shipping")
    inside_valley_charge = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    outside_valley_charge = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    free_inside_valley = models.BooleanField(default=False)
    free_delivery_all_nepal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=models.Q(is_active=True),
                name="single_active_shipping_config",
            )
        ]

    def calculate_fee(self, area, subtotal: Decimal):
        if self.free_delivery_all_nepal:
            return ZERO_DECIMAL
        if area == INSIDE_VALLEY and self.free_inside_valley:
            return ZERO_DECIMAL
        if area == INSIDE_VALLEY:
            return self.inside_valley_charge
        return self.outside_valley_charge

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="shipping_addresses"
    )
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    area = models.CharField(max_length=32, choices=DELIVERY_AREAS)
    district = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    address_line = models.TextField()
    landmark = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "is_default"])]

    def __str__(self):
        return f"{self.full_name} - {self.city}"
