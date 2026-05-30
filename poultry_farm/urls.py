from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('farms/', include('farms.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('notifications/', include('notifications.urls')),
    path('social/', include('social.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
