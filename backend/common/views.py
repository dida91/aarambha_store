from django.db.models import Sum
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.permissions import IsSeller
from common.response import api_response
from orders.models import Order


class AdminDashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        today = timezone.localdate()
        month_start = today.replace(day=1)

        base = Order.objects.all()
        data = {
            'total_orders': base.count(),
            'pending_orders': base.filter(status=Order.Status.PENDING).count(),
            'rejected_orders': base.filter(status=Order.Status.REJECTED).count(),
            'today_sales': str(
                base.filter(status=Order.Status.CONFIRMED, created_at__date=today)
                .aggregate(total=Coalesce(Sum('total_amount'), 0))['total']
            ),
            'month_sales': str(
                base.filter(status=Order.Status.CONFIRMED, created_at__date__gte=month_start)
                .aggregate(total=Coalesce(Sum('total_amount'), 0))['total']
            ),
            'monthly_trend': [
                {'month': row['month'].strftime('%Y-%m') if row['month'] else None, 'sales': str(row['sales'])}
                for row in base.filter(status=Order.Status.CONFIRMED)
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(sales=Coalesce(Sum('total_amount'), 0))
                .order_by('month')
            ],
        }
        return api_response(data=data)
