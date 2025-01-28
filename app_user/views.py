from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from MainApp.models import Post
from app_user.models import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def profile(request, pk):  # Используем pk вместо user_id
    user = get_object_or_404(User, id=pk)
    posts = Post.objects.filter(author=user).order_by('published_date')  # Исправлено здесь
    context = {
        'title': f'Профиль пользователя {user.username}',
        'user': user,
        'posts': posts,
    }
    return render(request, 'accounts/profile.html', context)


def bookmarks(request):
    return render(request, 'accounts/bookmarks.html', {'title': 'Закладки'})


def donations(request):
    return render(request, 'accounts/donations.html', {'title': 'Донаты'})


def settings(request):
    return render(request, 'accounts/settings.html', {'title': 'Настройки'})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-published_date')  # Получаем посты пользователя
    return render(request, 'accounts/user_profile.html', {
        'user': user,
        'posts': posts,  # Передаем посты в контекст
    })
