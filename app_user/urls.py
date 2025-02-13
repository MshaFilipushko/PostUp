from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('captcha/', include('captcha.urls')),  # Для работы капчи

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('donations/', views.donations, name='donations'),
    path('settings/', views.settings, name='settings'),

    path('subs/', views.subs, name='subs'),
    path('accounts/user/<str:username>/', views.user_profile, name='user_profile'),
    path('accounts/toggle_subscription/<str:username>/', views.toggle_subscription, name='toggle_subscription'),
    path('accounts/subscriptions/', views.subscriptions_list, name='subs'),
]
