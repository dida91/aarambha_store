from django.db.models import F
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import (
    AddToCartSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)
from catalog.models import Product
from common.permissions import IsCustomer
from common.response import build_envelope


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def _get_cart(self, user):
        return Cart.objects.get_or_create(user=user)[0]

    @action(detail=False, methods=["get"], url_path="health")
    def health(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store cart service is healthy",
                data={"service": "cart", "brand": "Aarambha Store"},
                errors=None,
            )
        )

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        cart = self._get_cart(request.user)
        data = CartSerializer(cart).data
        return Response(
            build_envelope(success=True, message="Cart fetched", data=data, errors=None)
        )

    @action(detail=False, methods=["post"], url_path="items")
    def add_item(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(
            id=serializer.validated_data["product_id"], is_active=True
        )
        cart = self._get_cart(request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": serializer.validated_data["quantity"]},
        )
        if not created:
            item.quantity = F("quantity") + serializer.validated_data["quantity"]
            item.save(update_fields=["quantity"])
            item.refresh_from_db()
        return Response(
            build_envelope(
                success=True,
                message="Item added to cart",
                data=CartSerializer(cart).data,
                errors=None,
            ),
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["patch"], url_path="items")
    def update_item(self, request, pk=None):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self._get_cart(request.user)
        item = CartItem.objects.get(id=pk, cart=cart)
        item.quantity = serializer.validated_data["quantity"]
        item.save(update_fields=["quantity", "updated_at"])
        return Response(
            build_envelope(
                success=True,
                message="Cart item updated",
                data=CartSerializer(cart).data,
                errors=None,
            )
        )

    @action(detail=True, methods=["delete"], url_path="items")
    def remove_item(self, request, pk=None):
        cart = self._get_cart(request.user)
        CartItem.objects.filter(id=pk, cart=cart).delete()
        return Response(
            build_envelope(
                success=True,
                message="Cart item removed",
                data=CartSerializer(cart).data,
                errors=None,
            )
        )
