from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.response import build_envelope
from orders.models import Order


class CommonHealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            build_envelope(
                success=True,
                message="Aarambha Store common service is healthy",
                data={"service": "common", "brand": "Aarambha Store"},
                errors=None,
            )
        )


class AdminMetricsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.localdate()
        month_start = today.replace(day=1)

        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
        rejected_orders = Order.objects.filter(status=Order.Status.REJECTED).count()

        today_sales = Order.objects.filter(
            status=Order.Status.CONFIRMED,
            created_at__date=today,
        ).aggregate(total=Sum("grand_total"))["total"] or Decimal("0.00")

        month_sales = Order.objects.filter(
            status=Order.Status.CONFIRMED,
            created_at__date__gte=month_start,
            created_at__date__lte=today,
        ).aggregate(total=Sum("grand_total"))["total"] or Decimal("0.00")

        return Response(
            build_envelope(
                success=True,
                message="Admin metrics fetched",
                data={
                    "total_orders": total_orders,
                    "pending_orders": pending_orders,
                    "rejected_orders": rejected_orders,
                    "today_sales": today_sales,
                    "month_sales": month_sales,
                },
                errors=None,
            )
        )
