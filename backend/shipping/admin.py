from django.contrib import admin

from shipping.models import ShippingAddress, ShippingConfig


@admin.register(ShippingConfig)
class ShippingConfigAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'inside_valley_charge',
        'outside_valley_charge',
        'free_inside_valley',
        'free_delivery_all_nepal',
        'is_active',
    )
    list_filter = ('is_active', 'free_inside_valley', 'free_delivery_all_nepal')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'area', 'district', 'city', 'is_default')
    list_filter = ('area', 'is_default')
    search_fields = ('full_name', 'phone', 'district', 'city')
