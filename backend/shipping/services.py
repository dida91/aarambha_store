from rest_framework.exceptions import ValidationError

from shipping.models import ShippingConfig


def get_active_shipping_config() -> ShippingConfig:
    config = ShippingConfig.objects.filter(is_active=True).first()
    if not config:
        raise ValidationError({"shipping": ["No active shipping configuration found."]})
    return config
