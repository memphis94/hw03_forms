from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator


from .forms import PostForm
from .models import Post, Group, User

def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'    
    context = {      
        'group': group,        
        'page_obj': page_obj,      
    }
    return render(request, template, context)

def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).select_related('author', 'group').order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    count = Post.objects.filter(author=author).count()
    context = {
        'author': author,
        'page_obj': page_obj,
        'count': count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)    
    template = 'posts/post_detail.html'
    context = {
        'post': post
    }    
    return render(request, template, context)


@login_required
def post_create(request):
    groups = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author.username)
    else:
        print(form.errors)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'groups': groups,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        template = 'posts:post_detail'
        post.save()
        return redirect(template, post_id=post.pk)
    groups = Group.objects.all()
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'groups': groups,
        'is_edit': is_edit
    }
    return render(request, template, context)