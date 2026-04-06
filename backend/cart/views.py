from decimal import Decimal

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import CartItem
from cart.serializers import CartItemSerializer
from common.response import api_response


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        subtotal = sum((item.product.price * Decimal(item.quantity) for item in queryset), Decimal('0.00'))
        return api_response(data={'items': serializer.data, 'subtotal': subtotal})

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        existing = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        if existing:
            serializer = self.get_serializer(existing, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return api_response(message='Cart item updated.', data=serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(message='Cart item added.', data=serializer.data, http_status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(message='Cart item updated.', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(message='Cart item removed.', data={})
