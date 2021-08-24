from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, User
from .models import Group
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    posts = Post.objects.filter(
        author=author)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'author': author
    }
    return render(request, template, context)


def post_detail(request, post_id):
    user_post = get_object_or_404(Post, pk=post_id)
    posts_count = user_post.author.posts.all().count()
    post_group = user_post.group
    context = {
        'user_post': user_post,
        'posts_count': posts_count,
        'post_group': post_group,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('posts:profile', username=request.user.username)
    return render(request, 'posts/create_post.html')


@login_required
def post_edit(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.author == request.user:
                post.save()
                return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/update_post.html', {'form': form})
    return render(request, 'posts/update_post.html')
