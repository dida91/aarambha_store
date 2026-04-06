from django.contrib import admin

from promotions.models import PromoCode, PromoUsage


class PromoUsageInline(admin.TabularInline):
    model = PromoUsage
    extra = 0
    readonly_fields = ('user', 'order', 'created_at')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'is_active', 'is_public', 'start_at', 'end_at')
    list_filter = ('is_active', 'is_public')
    search_fields = ('code', 'description')
    filter_horizontal = ('allowed_users',)
    inlines = [PromoUsageInline]
