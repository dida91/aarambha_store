from django.contrib import admin

from catalog.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'sku')
    list_filter = ('is_active',)
    inlines = [ProductImageInline]
