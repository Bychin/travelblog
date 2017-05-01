from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        label=u'Login',
        max_length=20
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
        label=u'Email',
        max_length=50
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form'}),
        min_length=6,
        label=u'Password',
        error_messages={'min_length': 'Пароль должен быть не менее 6 символов'}
    )

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6,
        label=u'Repeat_password',
        error_messages={'min_length': 'Пароль должен быть не менее 6 символов'}
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'Такой пользователь уже существует')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(u'Данная почта уже зарегистрирована!')
        except User.DoesNotExist:
            return email

    def clean_repeat_password(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['repeat_password']
        if pass1 != pass2:
            raise forms.ValidationError(u'Пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        new_user = User()
        new_user.username = data.get('username')
        new_user.password = make_password(password)
        new_user.email = data.get('email')
        new_user.is_active = True
        new_user.is_superuser = False
        new_user.save()
        return new_user
