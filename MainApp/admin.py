# MainApp/admin.py

from django.contrib import admin
from .models import Post, Bookmark, Subscription

# Регистрация модели Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    # Добавляем поле created_date, если оно необходимо
    def created_date(self, obj):
        return obj.created_date if hasattr(obj, 'created_date') else None

    created_date.admin_order_field = 'created_date'  # Позволяет сортировать по этому полю
    created_date.short_description = 'Created Date'

# Регистрация модели Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

# Регистрация модели Subscription
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'target_user', 'created_at')
    list_filter = ('subscriber', 'target_user', 'created_at')
    search_fields = ('subscriber__username', 'target_user__username')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']