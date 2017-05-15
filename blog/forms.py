from django.contrib.auth import authenticate
from django import forms
from .models import Post, Traveler


class LoginForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Имя', }
        ),
        max_length=30,
        label=u'Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '*******', }
        ),
        label=u'Пароль'
    )

    def clean(self):
        data = self.cleaned_data
        try:
            username_input = Traveler.objects.get(username=data['login'])
            user = authenticate(username=username_input, password=data['password'])
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(u'Данный пользователь не активен')
        except:
            raise forms.ValidationError(u'Указан неверный логин или пароль')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'longitude', 'latitude',
                  'longitude2', 'latitude2', 'longitude3', 'latitude3', 'img']
        widgets = {'title': forms.TextInput(attrs={'class': "form-control"}),
                   'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
                   'longitude': forms.HiddenInput(),
                   'latitude': forms.HiddenInput(),
                   'longitude2': forms.HiddenInput(),
                   'latitude2': forms.HiddenInput(),
                   'longitude3': forms.HiddenInput(),
                   'latitude3': forms.HiddenInput(),
                   }


class AddCommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 2, 'class': 'form-control'}
        ),
        label=u'text',
        required='true',
    )