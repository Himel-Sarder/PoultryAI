from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post_view, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment_view, name='add_comment'),
]
