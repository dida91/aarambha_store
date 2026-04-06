from django.urls import path

from orders.views import (
    CheckoutView,
    CustomerOrderDetailView,
    CustomerOrderListView,
    SellerOrderDetailView,
    SellerOrderListView,
    SellerOrderStatusUpdateView,
)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('me/', CustomerOrderListView.as_view(), name='customer-order-list'),
    path('me/<int:pk>/', CustomerOrderDetailView.as_view(), name='customer-order-detail'),
    path('seller/', SellerOrderListView.as_view(), name='seller-order-list'),
    path('seller/<int:pk>/', SellerOrderDetailView.as_view(), name='seller-order-detail'),
    path('seller/<int:order_id>/status/', SellerOrderStatusUpdateView.as_view(), name='seller-order-status-update'),
]
