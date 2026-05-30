from django.contrib import admin
from .models import FarmProfile


@admin.register(FarmProfile)
class FarmProfileAdmin(admin.ModelAdmin):
    list_display = ['farm_name', 'seller', 'location', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['farm_name', 'seller__email', 'location']
    actions = ['verify_farms']

    def verify_farms(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} farms verified.')
    verify_farms.short_description = 'Verify selected farms'
