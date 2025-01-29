from django.urls import path
from . import views
from .views import toggle_bookmark

urlpatterns = [
    path('', views.index, name='index'),  # Главная станичка на views в приложении
    path('about/', views.about, name='about'),  # Страничка о нас
    path('contact/', views.contact, name='contact'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детальная страница статьи
    path('post/new/', views.create_post, name='create_post'),  # Создание статьи
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),  # Редактирование статьи
    path("toggle_bookmark/<int:post_id>/", toggle_bookmark, name="toggle_bookmark"),

]
