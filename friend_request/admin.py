from django.contrib import admin
from .models import FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):

    list_display = ['id', 'from_user', 'to_user', 'created_at']
    list_display_links = ['id']
    ordering = ['id']
