from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView

from .models import Post, Bookmark, Subscription, Comment, Category
from .forms import PostForm, CommentForm


def index(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(published_date__isnull=False, category=category).order_by('-published_date')
    else:
        posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    bookmarks = Bookmark.objects.filter(user=request.user) if request.user.is_authenticated else None
    posts_with_bookmarks = []
    for post in posts:
        posts_with_bookmarks.append({
            'post': post,
            'is_bookmarked': bookmarks.filter(post=post).exists() if request.user.is_authenticated else False
        })
    context = {
        'title': 'Главная страница',
        'posts_with_bookmarks': posts_with_bookmarks,
        'categories': Category.objects.all(),
        'selected_category': category_slug
    }
    return render(request, 'users/main_page.html', context)


def category_posts(request, category_slug):
    return index(request, category_slug)


def about(request):
    return render(request, "users/about.html")


def contact(request):
    return render(request, "users/contact.html")


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:  # Если нажата кнопка "Опубликовать"
                post.status = 'published'  # Устанавливаем статус "опубликовано"
                post.publish()  # Устанавливаем дату публикации
            post.save()  # Сохраняем объект
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'site/create_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'publish' in request.POST:  # Если нажата кнопка "Опубликовать"
                post.publish()  # Устанавливаем дату публикации
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'site/edit_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().select_related('author').prefetch_related('replies')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'site/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # URL для перенаправления после удаления

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
    # Перенаправляем пользователя на ту же страницу, где он был
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def bookmarks_list(request):
    # Получаем все закладки пользователя и сортируем их по дате создания в обратном порядке
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post').order_by('-created_at')

    # Добавляем информацию о состоянии закладок (уже закладан или нет)
    for bookmark in bookmarks:
        bookmark.is_bookmarked = True  # Все посты в списке закладок уже закладаны

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'accounts/bookmarks.html', context)


def fresh_posts(request):
    posts_with_bookmarks = []
    if request.user.is_authenticated:
        posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
        bookmarks = Post.objects.filter(bookmarks__user=request.user)
        for post in posts:
            posts_with_bookmarks.append({
                'post': post,
                'is_bookmarked': post in bookmarks
            })
    else:
        posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
        for post in posts:
            posts_with_bookmarks.append({
                'post': post,
                'is_bookmarked': False
            })

    context = {
        'posts_with_bookmarks': posts_with_bookmarks,
    }
    return render(request, 'users/main_page.html', context)

@login_required
def subscribed_posts(request):
    # Получаем всех пользователей, на которых подписан текущий пользователь
    subscribed_users = request.user.subscriptions.values_list('target_user', flat=True)

    # Получаем все посты этих пользователей
    posts = Post.objects.filter(author__in=subscribed_users).order_by('-published_date')

    # Получаем все закладки текущего пользователя
    bookmarks = Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)

    # Формируем список постов с информацией о закладках
    posts_with_bookmarks = []
    for post in posts:
        posts_with_bookmarks.append({
            'post': post,
            'is_bookmarked': post.id in bookmarks
        })

    context = {
        'posts_with_bookmarks': posts_with_bookmarks,
    }
    return render(request, 'users/subscribed_posts.html', context)


def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user not in post.users_who_liked.all():
            post.likes += 1
            post.users_who_liked.add(request.user)
            if request.user in post.users_who_disliked.all():
                post.dislikes -= 1
                post.users_who_disliked.remove(request.user)
        else:
            post.likes -= 1
            post.users_who_liked.remove(request.user)
        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def toggle_dislike(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user not in post.users_who_disliked.all():
            post.dislikes += 1
            post.users_who_disliked.add(request.user)
            if request.user in post.users_who_liked.all():
                post.likes -= 1
                post.users_who_liked.remove(request.user)
        else:
            post.dislikes -= 1
            post.users_who_disliked.remove(request.user)
        post.save()
        return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def toggle_like_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user not in comment.users_who_liked.all():
            comment.likes += 1
            comment.users_who_liked.add(request.user)
            if request.user in comment.users_who_disliked.all():
                comment.dislikes -= 1
                comment.users_who_disliked.remove(request.user)
        else:
            comment.likes -= 1
            comment.users_who_liked.remove(request.user)
        comment.save()
        return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def toggle_dislike_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user not in comment.users_who_disliked.all():
            comment.dislikes += 1
            comment.users_who_disliked.add(request.user)
            if request.user in comment.users_who_liked.all():
                comment.likes -= 1
                comment.users_who_liked.remove(request.user)
        else:
            comment.dislikes -= 1
            comment.users_who_disliked.remove(request.user)
        comment.save()
        return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})
    return JsonResponse({'error': 'Invalid request'}, status=400)