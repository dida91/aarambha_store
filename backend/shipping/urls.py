from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shipping.views import ShippingConfigViewSet, ShippingHealthViewSet

router = DefaultRouter()
router.register("health", ShippingHealthViewSet, basename="shipping-health")
router.register("configs", ShippingConfigViewSet, basename="shipping-configs")

urlpatterns = [path("", include(router.urls))]
