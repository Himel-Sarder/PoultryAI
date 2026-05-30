from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list_view, name='chat_list'),
    path('<int:user_id>/', views.chat_detail_view, name='chat_detail'),
    path('ai/', views.ai_chat_view, name='ai_chat'),
    path('send/<int:user_id>/', views.send_message_view, name='send_message'),
]
