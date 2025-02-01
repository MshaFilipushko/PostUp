from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse

from MainApp.models import Post, Bookmark, Subscription
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





def bookmarks(request):
    return render(request, 'accounts/bookmarks.html', {'title': 'Закладки'})


def donations(request):
    return render(request, 'accounts/donations.html', {'title': 'Донаты'})


def settings(request):
    return render(request, 'accounts/settings.html', {'title': 'Настройки'})

def subs(request):
    return render(request, 'accounts/subs.html', {'title': 'Подписки'})


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-published_date')
    is_owner = request.user == profile_user  # Добавляем проверку владельца

    # Общая логика для закладок и подписок
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
        'is_owner': is_owner,  # Передаем в шаблон
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