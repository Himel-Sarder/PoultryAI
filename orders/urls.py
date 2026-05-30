from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_view, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.order_list_view, name='order_list'),
    path('<int:pk>/', views.order_detail_view, name='order_detail'),
    path('seller/<int:pk>/', views.seller_order_detail_view, name='seller_order_detail'),
    path('<int:pk>/cancel/', views.cancel_order_view, name='cancel_order'),
    path('<int:pk>/status/', views.update_order_status_view, name='update_status'),
]
