from django.urls import path

from cart.views import CartHealthView, MyCartView

urlpatterns = [
    path("health/", CartHealthView.as_view(), name="cart-health"),
    path("me/", MyCartView.as_view(), name="cart-me"),
]
