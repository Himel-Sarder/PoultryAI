from django.contrib import admin
from .models import FarmPost, PostLike, PostComment

@admin.register(FarmPost)
class FarmPostAdmin(admin.ModelAdmin):
    list_display = ['seller', 'content', 'created_at']
    search_fields = ['seller__email', 'content']
