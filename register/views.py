from django.shortcuts import render
from register.forms import SignupForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import redirect


def register(request):
    if request.user.is_active:
        return redirect('/profile/' + str(request.user) + '/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth.login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'register/signup.html', {'form': form})
