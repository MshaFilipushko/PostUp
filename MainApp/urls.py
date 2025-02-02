from django.urls import path
from . import views
from .views import DeletePostView, post_detail

urlpatterns = [
    path('', views.index, name='index'),  # Главная станичка на views в приложении
    path('about/', views.about, name='about'),  # Страничка о нас
    path('contact/', views.contact, name='contact'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детальная страница статьи
    path('post/new/', views.create_post, name='create_post'),  # Создание статьи
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),  # Редактирование статьи
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('bookmarks/toggle/<int:post_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/dislike/', views.toggle_dislike, name='toggle_dislike'),
    path('comment/<int:comment_id>/like/', views.toggle_like_comment, name='toggle_like_comment'),
    path('comment/<int:comment_id>/dislike/', views.toggle_dislike_comment, name='toggle_dislike_comment'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),  # Посты по категории
]