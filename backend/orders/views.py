from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from common.permissions import IsSeller
from common.response import api_response
from orders.models import Order
from orders.serializers import (
    CheckoutSerializer,
    OrderSerializer,
    SellerOrderStatusUpdateSerializer,
)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "checkout"

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.create_order(request.user)
        return api_response(
            message="Order placed successfully.",
            data=OrderSerializer(order).data,
            http_status=status.HTTP_201_CREATED,
        )


class CustomerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("items", "status_history")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(data=response.data)


class CustomerOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "items", "status_history"
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(data=response.data)


class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_queryset(self):
        return (
            Order.objects.all()
            .prefetch_related("items", "status_history")
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(data=response.data)


class SellerOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsSeller]
    queryset = Order.objects.all().prefetch_related("items", "status_history")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(data=response.data)


class SellerOrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def post(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return api_response(
                success=False,
                message="Order not found.",
                errors={"order_id": "Invalid order ID."},
                http_status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SellerOrderStatusUpdateSerializer(
            data=request.data, context={"order": order, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return api_response(
            message="Order status updated.", data=OrderSerializer(order).data
        )
