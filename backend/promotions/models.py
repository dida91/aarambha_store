from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=255, blank=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    min_cart_value = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=0, help_text='0 means unlimited')
    per_user_limit = models.PositiveIntegerField(default=1)
    is_public = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='allowed_promocodes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_at__gt=models.F('start_at')), name='promo_end_after_start'),
            models.CheckConstraint(check=models.Q(per_user_limit__gte=1), name='promo_per_user_limit_gte_1'),
        ]

    def clean(self):
        if self.end_at <= self.start_at:
            raise ValidationError('Promo end_at must be after start_at.')

    def is_valid_for(self, user, cart_subtotal):
        now = timezone.now()
        if not self.is_active or now < self.start_at or now > self.end_at:
            return False, 'Promo code is not active in current date window.'
        if cart_subtotal < self.min_cart_value:
            return False, 'Minimum cart value not met.'
        if self.usage_limit and self.usages.count() >= self.usage_limit:
            return False, 'Promo usage limit reached.'
        if not self.is_public and user not in self.allowed_users.all():
            return False, 'Promo not allowed for this user.'
        user_usage_count = self.usages.filter(user=user).count()
        if user_usage_count >= self.per_user_limit:
            return False, 'Per-user usage limit reached.'
        return True, 'Promo is valid.'

    def __str__(self):
        return self.code


class PromoUsage(models.Model):
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promo_usages')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='promo_usages')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['promo', 'order'], name='unique_promo_usage_order')
        ]
