from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.exceptions import ValidationError
from .models import Post
from .forms import LoginForm, AddPostForm, AddCommentForm, PostForm


def home(request):
    return render(request, 'admin/home.html', {})


def my_login(request):
    if request.user.is_authenticated():
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
    user = get_object_or_404(User, username=user_name)
    #user = User.objects.get(username=user_name)
    posts = Post.objects.filter(author=user, published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'admin/account.html', {'posts': posts})


def post_new(request):
    if request.method == "POST":
        post = Post(author=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post_ = form.save(commit=False)

            try:
                post_.full_clean()
            except ValidationError:
                messages.error(request,
                               f"Title should contain {Post._meta.get_field('title').max_length} characters or less")
            else:
                post_.publish()
                form.save()
                return redirect('account', request.user)
    else:
        form = PostForm()
    return render(request, 'admin/add_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = AddCommentForm(request.POST)
    if request.user.is_authenticated():
        if 'like_button' in request.POST:
            post.rating.add_like(request.user)
            post.rating.save()
        elif 'dislike_button' in request.POST:
            post.rating.add_dislike(request.user)
            post.rating.save()
        elif form.is_valid():
            post.add_comment(request.user, form.cleaned_data['text'])
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return render(request, 'admin/post.html', {'post': post, 'form': form})
        return render(request, 'admin/login.html', {'form': form})
    return render(request, 'admin/post.html', {'post': post, 'form': AddCommentForm()})