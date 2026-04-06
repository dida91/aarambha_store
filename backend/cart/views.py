from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from common.response import build_envelope


class CartHealthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Cart service is healthy",
                data={"service": "cart"},
                errors=None,
            )
        )


class MyCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = list(
            cart.items.select_related("product")
            .order_by("id")
            .values("id", "product_id", "product__name", "quantity")
        )
        return Response(
            build_envelope(
                success=True,
                message="Cart fetched",
                data={"id": cart.id, "items": items},
                errors=None,
            )
        )
