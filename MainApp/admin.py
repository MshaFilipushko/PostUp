from django.contrib import admin
from .models import Post, Comment, Bookmark, Subscription, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_date', 'category')
    list_filter = ('author', 'published_date', 'category')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    def created_date(self, obj):
        return obj.created_date if hasattr(obj, 'created_date') else None

    created_date.admin_order_field = 'created_date'  # Позволяет сортировать по этому полю
    created_date.short_description = 'Created Date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'likes', 'dislikes')
    list_filter = ('author', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'target_user', 'created_at')
    list_filter = ('subscriber', 'target_user', 'created_at')
    search_fields = ('subscriber__username', 'target_user__username')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']