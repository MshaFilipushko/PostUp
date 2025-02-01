from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse

from MainApp.models import Post, Bookmark, Subscription
from app_user.models import CustomUserCreationForm, Profile


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def bookmarks(request):
    return render(request, 'accounts/bookmarks.html', {'title': 'Закладки'})


def donations(request):
    return render(request, 'accounts/donations.html', {'title': 'Донаты'})


def subs(request):
    return render(request, 'accounts/subs.html', {'title': 'Подписки'})


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-published_date')
    is_owner = request.user == profile_user  # Проверяем, является ли текущий пользователь владельцем профиля

    # Логика для закладок и подписок
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(user=request.user)
        subscriptions = Subscription.objects.filter(subscriber=request.user)
        for post in posts:
            post.is_bookmarked = bookmarks.filter(post=post).exists()
        is_subscribed = subscriptions.filter(target_user=profile_user).exists()
    else:
        for post in posts:
            post.is_bookmarked = False
        is_subscribed = False

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_subscribed': is_subscribed,
        'is_owner': is_owner,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required
def toggle_subscription(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect(reverse('user_profile', args=[username]))

    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        target_user=target_user
    )

    if not created:
        subscription.delete()

    # Редирект на предыдущую страницу (если есть HTTP_REFERER, иначе на профиль пользователя)
    return redirect(request.META.get('HTTP_REFERER', reverse('user_profile', args=[username])))


@login_required
def subscriptions_list(request):
    user_subscriptions = request.user.subscriptions.all()
    subscribed_users = [subscription.target_user for subscription in user_subscriptions]

    context = {
        'subscribed_users': subscribed_users,
    }
    return render(request, 'accounts/subs.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        age = request.POST.get('age')  # Новое поле
        bio = request.POST.get('bio')  # Новое поле

        # Проверяем уникальность имени пользователя
        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, 'Имя пользователя уже занято.')
        elif User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, 'Этот email уже используется другим пользователем.')
        else:
            # Обновляем данные пользователя
            request.user.username = username
            request.user.email = email
            request.user.first_name = first_name
            request.user.save()

            # Обновляем данные профиля
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.age = age or None  # Сохраняем возраст (если указан)
            profile.bio = bio  # Сохраняем "О себе"
            profile.save()

            messages.success(request, 'Настройки успешно сохранены.')
            return redirect('settings')  # Перенаправляем обратно на страницу настроек

    # Загружаем текущие данные пользователя и профиля
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'accounts/settings.html', context)
