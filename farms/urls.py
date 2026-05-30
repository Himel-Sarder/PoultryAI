from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('', views.farm_list_view, name='farm_list'),
    path('<int:pk>/', views.farm_detail_view, name='farm_detail'),
    path('create/', views.create_farm_view, name='create_farm'),
    path('edit/', views.edit_farm_view, name='edit_farm'),
    path('my-farm/', views.my_farm_view, name='my_farm'),
]
