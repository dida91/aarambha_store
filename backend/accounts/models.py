from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimestampedModel


class User(TimestampedModel, AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        SELLER = "SELLER", "Seller"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        indexes = [models.Index(fields=["role"]), models.Index(fields=["email"])]

    def __str__(self):
        return self.username
