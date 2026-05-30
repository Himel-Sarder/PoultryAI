from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Review


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'seller', 'total_amount', 'status', 'payment_verified', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_verified']
    search_fields = ['buyer__email', 'seller__email', 'transaction_id']
    list_editable = ['status', 'payment_verified']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'rating', 'created_at']
    list_filter = ['rating']
