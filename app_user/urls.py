from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('captcha/', include('captcha.urls')),  # Для работы капчи

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('donations/', views.donations, name='donations'),
    path('settings/', views.settings, name='settings'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

]
