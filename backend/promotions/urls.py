from django.urls import include, path
from rest_framework.routers import DefaultRouter

from promotions.views import PromoCodeViewSet, PromotionsHealthViewSet

router = DefaultRouter()
router.register("health", PromotionsHealthViewSet, basename="promotions-health")
router.register("codes", PromoCodeViewSet, basename="promotions-codes")

urlpatterns = [path("", include(router.urls))]
