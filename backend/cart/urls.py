from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cart.views import CartItemViewSet

router = DefaultRouter()
router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
]
