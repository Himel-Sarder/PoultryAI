from django.contrib import admin
from .models import Product, ProductImage, Coupon


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'unit', 'quantity', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_featured']
    search_fields = ['name', 'seller__email']
    list_editable = ['is_available', 'is_featured']
    inlines = [ProductImageInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'min_order_amount', 'max_uses', 'used_count', 'is_active', 'valid_to']
    list_filter = ['is_active']
    search_fields = ['code']
