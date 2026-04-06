from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipping.views import ShippingAddressViewSet, ShippingConfigViewSet

router = DefaultRouter()
router.register("configs", ShippingConfigViewSet, basename="shipping-configs")
router.register("addresses", ShippingAddressViewSet, basename="shipping-addresses")

urlpatterns = [
    path("", include(router.urls)),
]
