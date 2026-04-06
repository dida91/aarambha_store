from decimal import Decimal

from shipping.models import ShippingConfig


def test_shipping_fee_inside_valley_free_toggle():
    config = ShippingConfig(
        free_delivery_all_nepal=False,
        free_inside_valley=True,
        inside_valley_fee=Decimal("100.00"),
        outside_valley_fee=Decimal("250.00"),
    )
    assert config.calculate_delivery_fee(ShippingConfig.Zone.INSIDE_VALLEY) == Decimal(
        "0.00"
    )


def test_shipping_fee_all_nepal_free_toggle():
    config = ShippingConfig(
        free_delivery_all_nepal=True,
        free_inside_valley=False,
        inside_valley_fee=Decimal("100.00"),
        outside_valley_fee=Decimal("250.00"),
    )
    assert config.calculate_delivery_fee(ShippingConfig.Zone.OUTSIDE_VALLEY) == Decimal(
        "0.00"
    )
