from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from .models import Post

from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import PointField


class LoginForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Login', }
        ),
        max_length=30,
        label=u'login'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '*******', }
        ),
        label=u'password'
    )

    def clean(self):
        data = self.cleaned_data
        try:
            username_input = User.objects.get(username=data['login'])
            user = authenticate(username=username_input, password=data['password'])
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(u'Данный пользователь не активен')
        except:
            raise forms.ValidationError(u'Указан неверный логин или пароль')


class PostForm(forms.ModelForm):
    #geom = PointField()
    class Meta:
        model = Post
        fields = ['title', 'text', 'geom'] #, 'image'
        widgets = {'title': forms.TextInput(attrs={'class': "form-control"}),
                    'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
                    'geom': LeafletWidget(),
                   #'image': forms.FileInput(),
                  }


class AddCommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 2, 'class': 'form-control'}
        ),
        label=u'text',
        required='true',
    )
