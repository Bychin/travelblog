from django.shortcuts import render
from register.forms import SignupForm
from django.contrib import auth
from django.shortcuts import redirect


def register(request):
    if request.user.is_authenticated():
        return redirect('/profile/' + str(request.user) + '/posts/')
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            new_user.avatar = form.cleaned_data['image']
            auth.login(request, new_user)
            return redirect('/profile/' + str(form.cleaned_data['username']) + '/posts/')
    else:
        form = SignupForm()
    return render(request, 'register/signup.html', {'form': form})
