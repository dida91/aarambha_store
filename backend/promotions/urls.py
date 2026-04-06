from django.urls import include, path
from rest_framework.routers import DefaultRouter

from promotions.views import PromoCodeViewSet

router = DefaultRouter()
router.register("codes", PromoCodeViewSet, basename="promo-codes")

urlpatterns = [
    path("", include(router.urls)),
]
