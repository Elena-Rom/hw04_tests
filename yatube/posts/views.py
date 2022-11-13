from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import paginate_page

PAGE_REPEAT = 10


def index(request):
    post_list = Post.objects.all()[:PAGE_REPEAT]
    paginator = paginate_page(
        request=request,
        post_list=post_list,
    )
    context = {
        'page_obj': paginator,
        'posts': post_list,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = paginate_page(
        request=request,
        post_list=posts,
    )
    context = {
        'posts': posts,
        'group': group,
        'page_obj': paginator,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = paginate_page(
        request=request,
        post_list=posts,
    )
    context = {
        'author': author,
        'page_obj': paginator,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect(
            'posts:post_detail', post_id=post_id
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_edit', post_id=post_id)
    return render(
        request,
        'posts/create_post.html',
        {
            'form': form,
            'post': post,
        }
    )
