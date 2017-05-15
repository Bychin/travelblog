from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.models import Traveler


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    about = forms.TextInput()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Traveler
        fields = ('username', 'email', 'password', 'about', 'avatar')

