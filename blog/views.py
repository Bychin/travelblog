from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.exceptions import ValidationError
from .models import Post
from blog.forms import LoginForm, AddPostForm
from .models import Post, PostForm



def home(request):
    return render(request, 'admin/home.html', {})


def my_login(request):
    if request.user.is_active:
        return redirect('/profile/' + str(request.user) + '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return redirect('/profile/' + str(form.cleaned_data['login']) + '/')
    else:
        form = LoginForm()
    return render(request, 'admin/login.html', {'form': form})


def account(request, user_name):
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(author=user, published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'admin/account.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'admin/post.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        post = Post(author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post_ = form.save(commit=False)
            form.save()
            post_.publish()
            return redirect('account', request.user)
    else:
        form = PostForm()
    return render(request, 'admin/add_post.html', {'form': form})
