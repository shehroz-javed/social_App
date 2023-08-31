from django.contrib import admin
from .models import Post, Like, Comment


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):

    list_display = ['id', 'description', 'user', 'post_type']
    list_display_links = ['id', 'description']
    list_filter = ['user']
    ordering = ['-id']
    list_per_page = 10


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'post']
    ordering = ['-id']
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ['id', 'comment', 'user', 'post']
    list_display_links = ['id', 'user']
    list_per_page = 10
