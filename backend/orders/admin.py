from django.contrib import admin

from orders.models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product",
        "product_name_snapshot",
        "unit_price_snapshot",
        "quantity",
        "line_total",
    )


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("from_status", "to_status", "actor", "note", "created_at")


@admin.action(description="Mark selected orders as CONFIRMED")
def mark_confirmed(modeladmin, request, queryset):
    for order in queryset.filter(status=Order.Status.PENDING):
        previous = order.status
        order.status = Order.Status.CONFIRMED
        order.save(update_fields=["status", "updated_at"])
        OrderStatusHistory.objects.create(
            order=order,
            from_status=previous,
            to_status=order.status,
            actor=request.user,
            note="Updated from admin action.",
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "user__email")
    actions = [mark_confirmed]
    inlines = [OrderItemInline, OrderStatusHistoryInline]
