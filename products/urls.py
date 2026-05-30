from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
    path('<int:pk>/review/', views.add_review_view, name='add_review'),
    path('my-products/', views.seller_product_list_view, name='seller_products'),
    path('add/', views.add_product_view, name='add_product'),
    path('<int:pk>/edit/', views.edit_product_view, name='edit_product'),
    path('<int:pk>/delete/', views.delete_product_view, name='delete_product'),
    path('image/<int:pk>/delete/', views.delete_product_image_view, name='delete_image'),
    path('validate-coupon/', views.validate_coupon_view, name='validate_coupon'),
]
