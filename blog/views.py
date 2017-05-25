from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import auth, messages
from .forms import *
from .models import Post, Rating, Comment
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password


def home(request):
    if request.user.is_authenticated():
        return render(request, 'admin/home.html', {'traveler':  request.user})
    else:
        return render(request, 'admin/home.html')


def error_404(request):
    return render(request, 'admin/404.html', {'traveler': request.user})


def my_login(request):
    if request.user.is_authenticated():
        return redirect('/profile/' + str(request.user) + '/posts/page1/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return redirect('/profile/' + str(form.cleaned_data['login']) + '/posts/page1/')
    else:
        form = LoginForm()
    return render(request, 'admin/login.html', {'form': form})


def posts(request):
    return redirect('/posts/page1')


def account(request, user_name):
    return redirect('/profile/' + user_name + '/posts/page1')


def account_settings(request):
    if not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return render(request, 'admin/account_settings.html', {'form': SettingsForm(), 'traveler': request.user})
        return render(request, 'admin/login.html', {'form': form})
    user = get_object_or_404(Traveler, username=request.user.username)
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        form.old_email = user.email
        form.username = user.username
        if form.is_valid():
            if form.cleaned_data['old_password'] and form.cleaned_data['new_password'] and form.cleaned_data['repeat_password']:
                user.password = make_password(form.cleaned_data['new_password'])
                user.save()
                auth.login(request, user)
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
                user.save()
            if form.cleaned_data['about']:
                user.about = form.cleaned_data['about']
                user.save()
            if form.cleaned_data['image']:
                user.avatar = form.cleaned_data['image']
                user.save()
            return HttpResponseRedirect(reverse('account_settings'))
    else:
        form = SettingsForm(initial={'email': user.email, 'about': user.about})
    return render(request, 'admin/account_settings.html', {'form': form, 'traveler': request.user})


def account_posts(request, user_name, num=1):
    if not num:
        num = 1
    num = int(num)
    page_posts_number = 10
    lower_bound = page_posts_number * (num - 1)
    upper_bound = page_posts_number * num
    user = get_object_or_404(Traveler, username=user_name)
    posts = Post.objects.filter(author=user).order_by('-published_date')
    posts_number = len(posts)
    pages = posts_number // page_posts_number
    if pages == 0:
        pages = 1
    if posts_number < lower_bound:
        lower_bound = pages * page_posts_number
        upper_bound = posts_number - 1
    posts = posts[lower_bound:upper_bound]
    prev_page = num - 1 if num - 1 > 0 else 1
    next_page = num + 1 if num + 1 <= pages else pages
    traveler = ""
    if request.user.is_authenticated():
        traveler = request.user
        for post in posts:
            if 'like_button'+str(post.id) in request.POST:
                post.rating.add_like(Traveler.objects.get(username=request.user))
                post.rating.save()
            elif 'dislike_button'+str(post.id) in request.POST:
                post.rating.add_dislike(Traveler.objects.get(username=request.user))
                post.rating.save()
    else:
        traveler = None
    return render(request, 'admin/account_posts.html', {'posts': posts, 'traveler': traveler, 'author': user,
                                                    'prev': prev_page, 'next': next_page, 'pages': pages})


def post_new(request):
    if not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(reverse('post_new'))
        return render(request, 'admin/login.html', {'form': form})
    if request.method == "POST":
        post = Post(author=request.user)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(post)
            post.publish()
            return redirect('account_posts', request.user, '1')
    else:
        form = PostForm()
    return render(request, 'admin/add_post.html', {'form': form, 'traveler': request.user})


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
        elif 'delete_button' in request.POST:
            Rating.objects.filter(post=post.id).delete()
            Comment.objects.filter(post=post.id).delete()
            Post.objects.filter(id=post.id).delete()
            return redirect('account_posts', request.user, '1')
        elif form.is_valid():
            post.add_comment(Traveler.objects.get(username=request.user), form.cleaned_data['text'])
            return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': pk}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return render(request, 'admin/post.html', {'post': post, 'form': form, 'traveler': request.user})
        return render(request, 'admin/login.html', {'form': form})
    return render(request, 'admin/post.html', {'post': post, 'form': AddCommentForm(), 'traveler': request.user})


def all_posts(request, num=1):
    if not num:
        num = 1
    num = int(num)
    page_posts_number = 10
    lower_bound = page_posts_number * (num - 1)
    upper_bound = page_posts_number * num
    posts = Post.objects.order_by('-published_date')
    posts_number = len(posts)
    pages = posts_number // page_posts_number
    if pages == 0:
        pages = 1
    if posts_number < lower_bound:
        lower_bound = pages * page_posts_number
        upper_bound = posts_number
    posts = posts[lower_bound:upper_bound]
    prev_page = num - 1 if num - 1 > 0 else 1
    next_page = num + 1 if num + 1 <= pages else pages
    traveler = ""
    if request.user.is_authenticated():
        traveler = request.user
        for post in posts:
            if 'like_button' + str(post.id) in request.POST:
                post.rating.add_like(Traveler.objects.get(username=request.user))
                post.rating.save()
            elif 'dislike_button' + str(post.id) in request.POST:
                post.rating.add_dislike(Traveler.objects.get(username=request.user))
                post.rating.save()
    else:
        traveler = None
    return render(request, 'admin/all_posts.html', {'posts': posts, 'traveler': traveler, 'prev': prev_page,
                                                    'next': next_page, 'pages': pages})
