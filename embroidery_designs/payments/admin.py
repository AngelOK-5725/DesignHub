from django.contrib import admin

# Register your models here.
# embroidery_designs/payments/admin.py
from django.contrib import admin
from .models import Purchase, Discount, Price

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'design', 'amount', 'discount_percent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'design__title')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('design', 'percent', 'active', 'start_date', 'end_date')
    list_filter = ('active',)
    list_editable = ('percent', 'active')
    readonly_fields = ('active',)  # чтобы админка не давала случайно активировать истекшую скидку



@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('design', 'amount', 'currency')
    list_editable = ('amount',)
