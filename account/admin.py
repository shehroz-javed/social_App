from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, Friends

# User model admin


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ['id', 'username', 'email', 'is_active', 'is_staff']
    list_editable = ['is_active']
    list_filter = ['is_active']
    list_display_links = ['id', 'username']
    search_fields = ['email', 'username']
    ordering = ['id']

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["username"]}),
        ("Permissions", {"fields": ["is_active", 'is_staff', 'is_superuser']}),
        ('Date Joined', {"fields": ["date_joined"]}),
        ('Last Login', {"fields": ["last_login"]})
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]

# Profile model admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['id',  'user', 'bio',]
    list_display_links = ['id', 'bio']
    ordering = ['id']
    readonly_fields = ['friends']


@admin.register(Friends)
class FriendAdmin(admin.ModelAdmin):

    list_display = ['id', 'follower', 'followed']
    list_display_links = ['id']
    ordering = ['id']
