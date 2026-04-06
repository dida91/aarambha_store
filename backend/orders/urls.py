from django.urls import path

from orders.views import MyOrderListView, OrdersHealthView

urlpatterns = [
    path("health/", OrdersHealthView.as_view(), name="orders-health"),
    path("me/", MyOrderListView.as_view(), name="orders-me"),
]
