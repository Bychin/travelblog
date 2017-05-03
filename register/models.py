from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

