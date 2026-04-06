from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone

from orders.models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "grand_total", "created_at")
    list_filter = ("status",)
    search_fields = ("id", "user__username", "user__email")
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    actions = ["mark_confirmed", "mark_rejected"]

    def changelist_view(self, request, extra_context=None):
        today = timezone.localdate()
        month_start = today.replace(day=1)

        extra = {
            "dashboard_metrics": {
                "total_orders": Order.objects.count(),
                "pending_orders": Order.objects.filter(
                    status=Order.Status.PENDING
                ).count(),
                "rejected_orders": Order.objects.filter(
                    status=Order.Status.REJECTED
                ).count(),
                "today_sales": (
                    Order.objects.filter(
                        status=Order.Status.CONFIRMED, created_at__date=today
                    ).aggregate(total=Sum("grand_total"))["total"]
                    or Decimal("0.00")
                ),
                "month_sales": (
                    Order.objects.filter(
                        status=Order.Status.CONFIRMED,
                        created_at__date__gte=month_start,
                        created_at__date__lte=today,
                    ).aggregate(total=Sum("grand_total"))["total"]
                    or Decimal("0.00")
                ),
            }
        }
        if extra_context:
            extra.update(extra_context)
        return super().changelist_view(request, extra_context=extra)

    @admin.action(description="Mark selected orders as confirmed")
    def mark_confirmed(self, request, queryset):
        for order in queryset:
            if order.can_transition_to(Order.Status.CONFIRMED):
                order.status = Order.Status.CONFIRMED
                order.rejection_reason = None
                order.save(update_fields=["status", "rejection_reason", "updated_at"])
                OrderStatusHistory.objects.create(
                    order=order,
                    status=Order.Status.CONFIRMED,
                    actor=request.user,
                    note="Marked confirmed from admin action.",
                )

    @admin.action(description="Mark selected orders as rejected")
    def mark_rejected(self, request, queryset):
        for order in queryset:
            if order.can_transition_to(Order.Status.REJECTED):
                order.status = Order.Status.REJECTED
                order.rejection_reason = "Rejected by admin action."
                order.save(update_fields=["status", "rejection_reason", "updated_at"])
                OrderStatusHistory.objects.create(
                    order=order,
                    status=Order.Status.REJECTED,
                    actor=request.user,
                    note="Marked rejected from admin action.",
                )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "quantity", "line_total")
    search_fields = ("product_name", "order__id")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "actor", "created_at")
    list_filter = ("status",)
