from django.contrib import admin

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

    @admin.action(description="Mark selected orders as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Order.Status.CONFIRMED, rejection_reason=None)

    @admin.action(description="Mark selected orders as rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status=Order.Status.REJECTED)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "quantity", "line_total")
    search_fields = ("product_name", "order__id")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "actor", "created_at")
    list_filter = ("status",)
