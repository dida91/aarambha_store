from django.db.models import Prefetch
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsCustomer, IsSellerOrAdmin
from common.response import build_envelope
from orders.models import Order, OrderStatusHistory
from orders.serializers import (
    CheckoutSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
)
from orders.services import create_order_from_cart, update_order_status


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    filterset_fields = ["status"]
    search_fields = ["id", "shipping_snapshot__address", "shipping_snapshot__city"]
    ordering_fields = ["created_at", "grand_total", "status"]

    def get_queryset(self):
        queryset = Order.objects.select_related("user").prefetch_related(
            "items",
            Prefetch(
                "status_history",
                queryset=OrderStatusHistory.objects.select_related("actor"),
            ),
        )
        if self.request.user.is_superuser or self.request.user.role in {
            "SELLER",
            "ADMIN",
        }:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in {"checkout", "customer_list", "customer_detail"}:
            return [permissions.IsAuthenticated(), IsCustomer()]
        if self.action in {"seller_list", "update_status"}:
            return [permissions.IsAuthenticated(), IsSellerOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="health", permission_classes=[])
    def health(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store orders service is healthy",
                data={"service": "orders", "brand": "Aarambha Store"},
                errors=None,
            )
        )

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        self.throttle_scope = "checkout"
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        order = create_order_from_cart(
            user=request.user,
            zone=payload["zone"],
            address=payload["address"],
            city=payload["city"],
            contact_phone=payload["contact_phone"],
            promo_code=payload.get("promo_code"),
        )

        data = OrderSerializer(order).data
        return Response(
            build_envelope(
                success=True,
                message="Order created successfully",
                data=data,
                errors=None,
            ),
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="my-orders")
    def customer_list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(OrderSerializer(page, many=True).data)
        return Response(
            build_envelope(
                success=True,
                message="Orders fetched",
                data=OrderSerializer(queryset, many=True).data,
                errors=None,
            )
        )

    @action(detail=True, methods=["get"], url_path="my-order")
    def customer_detail(self, request, pk=None):
        order = self.get_queryset().filter(user=request.user, pk=pk).first()
        if order is None:
            return Response(
                build_envelope(
                    success=False,
                    message="Order not found",
                    data=None,
                    errors={"detail": ["Not found."]},
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            build_envelope(
                success=True,
                message="Order fetched",
                data=OrderSerializer(order).data,
                errors=None,
            )
        )

    @action(detail=False, methods=["get"], url_path="seller/orders")
    def seller_list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(OrderSerializer(page, many=True).data)
        return Response(
            build_envelope(
                success=True,
                message="Seller orders fetched",
                data=OrderSerializer(queryset, many=True).data,
                errors=None,
            )
        )

    @action(detail=True, methods=["post"], url_path="seller/status")
    def update_status(self, request, pk=None):
        order = self.get_queryset().filter(pk=pk).first()
        if order is None:
            return Response(
                build_envelope(
                    success=False,
                    message="Order not found",
                    data=None,
                    errors={"detail": ["Not found."]},
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_order = update_order_status(
            order=order,
            actor=request.user,
            status=serializer.validated_data["status"],
            note=serializer.validated_data.get("note", ""),
            rejection_reason=serializer.validated_data.get("rejection_reason", ""),
        )
        return Response(
            build_envelope(
                success=True,
                message="Order status updated",
                data=OrderSerializer(updated_order).data,
                errors=None,
            )
        )
