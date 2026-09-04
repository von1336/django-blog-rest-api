from django.contrib import admin
from .models import Comment, Like, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
