from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная станичка на views в приложении
    path('about/', views.about, name='about'),  # Страничка о нас
    path('contact/', views.contact, name='contact')
]
