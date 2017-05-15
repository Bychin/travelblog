from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib import auth, messages
from django.core.exceptions import ValidationError
from .models import *
from .forms import LoginForm, AddCommentForm, PostForm


def home(request):
    if request.user.is_authenticated():
        return render(request,'admin/home.html',{'traveler':  request.user})
    else:
        return render(request, 'admin/home.html')


def error_404(request):
    return render(request, 'admin/404.html', {})


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
    user = get_object_or_404(Traveler, username=user_name)
    return render(request, 'admin/account.html', {'traveler': user})


def account_settings(request):
    #user = get_object_or_404(Traveler, username=user_name)
    if request.user.is_authenticated():
        return render(request, 'admin/account_settings.html', {'traveler': Traveler()})
    else:
        form = LoginForm()
        return render(request, 'admin/login.html', {'form': form})


def account_posts(request, user_name):
    user = get_object_or_404(Traveler, username=user_name)
    posts = Post.objects.filter(author=user).order_by('-published_date')

    return render(request, 'admin/account_posts.html', {'posts': posts})


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
                               "Error in fields!")
            else:
                post_.publish()
                form.save()
                return redirect('account_posts', request.user)
    else:
        form = PostForm()
    return render(request, 'admin/add_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = AddCommentForm(request.POST)
    if request.user.is_authenticated():
        if 'like_button' in request.POST:
            post.rating.add_like(Traveler.objects.get(username=request.user))
            post.rating.save()
        elif 'dislike_button' in request.POST:
            post.rating.add_dislike(Traveler.objects.get(username=request.user))
            post.rating.save()
        elif form.is_valid():
            post.add_comment(Traveler.objects.get(username=request.user), form.cleaned_data['text'])
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return render(request, 'admin/post.html', {'post': post, 'form': form})
        return render(request, 'admin/login.html', {'form': form})
    return render(request, 'admin/post.html', {'post': post, 'form': AddCommentForm()})
