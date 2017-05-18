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
        fields = ['title', 'text', 'places_count',
                  'longitude1', 'latitude1',
                  'longitude2', 'latitude2',
                  'longitude3', 'latitude3',
                  'longitude4', 'latitude4',
                  'longitude5', 'latitude5',
                  'longitude6', 'latitude6',
                  'longitude7', 'latitude7',
                  'longitude8', 'latitude8',
                  'longitude9', 'latitude9',
                  'longitude10', 'latitude10',
                  'img']
        widgets = {'title': forms.TextInput(attrs={'class': "form-control"}),
                   'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
                   'places_count': forms.HiddenInput(),
                   'longitude1': forms.HiddenInput(),
                   'latitude1': forms.HiddenInput(),
                   'longitude2': forms.HiddenInput(),
                   'latitude2': forms.HiddenInput(),
                   'longitude3': forms.HiddenInput(),
                   'latitude3': forms.HiddenInput(),
                   'longitude4': forms.HiddenInput(),
                   'latitude4': forms.HiddenInput(),
                   'longitude5': forms.HiddenInput(),
                   'latitude5': forms.HiddenInput(),
                   'longitude6': forms.HiddenInput(),
                   'latitude6': forms.HiddenInput(),
                   'longitude7': forms.HiddenInput(),
                   'latitude7': forms.HiddenInput(),
                   'longitude8': forms.HiddenInput(),
                   'latitude8': forms.HiddenInput(),
                   'longitude9': forms.HiddenInput(),
                   'latitude9': forms.HiddenInput(),
                   'longitude10': forms.HiddenInput(),
                   'latitude10': forms.HiddenInput(),
                   }


class AddCommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 2, 'class': 'form-control'}
        ),
        label=u'text',
        required='true',
    )