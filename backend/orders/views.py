from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope
from orders.models import Order


class OrdersHealthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Orders service is healthy",
                data={"service": "orders"},
                errors=None,
            )
        )


class MyOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = list(
            Order.objects.filter(user=request.user)
            .order_by("-created_at")
            .values(
                "id",
                "status",
                "subtotal",
                "discount_total",
                "shipping_fee",
                "grand_total",
                "created_at",
            )
        )
        return Response(
            build_envelope(
                success=True,
                message="Orders fetched",
                data=orders,
                errors=None,
            )
        )
