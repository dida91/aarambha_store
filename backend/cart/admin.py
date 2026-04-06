from django.contrib import admin

from cart.models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'updated_at')
    search_fields = ('user__username', 'product__name', 'product__sku')
