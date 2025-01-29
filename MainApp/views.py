from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView

from .models import Post, Bookmark
from .forms import PostForm


@login_required
def index(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    bookmarks = Bookmark.objects.filter(user=request.user)
    posts_with_bookmarks = []
    for post in posts:
        posts_with_bookmarks.append({
            'post': post,
            'is_bookmarked': bookmarks.filter(post=post).exists()
        })
    context = {
        'title': 'Главная страница',
        'posts_with_bookmarks': posts_with_bookmarks,
    }
    return render(request, 'users/main_page.html', context)


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
    return render(request, 'site/post_detail.html', {'post': post})


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
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post')
    return render(request, 'accounts/bookmarks.html', {'bookmarks': bookmarks})
