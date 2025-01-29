from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView

from .models import Post
from .forms import PostForm


def index(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    context = {
        'title': 'Главная страница',
        'posts': posts,
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
