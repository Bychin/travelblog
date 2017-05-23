from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.hashers import make_password
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


class SettingsForm(forms.Form):
    old_email = ""
    username = ""

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
        label=u'Новый адрес',
        max_length=100,
        required=False,
    )

    about = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label=u'Расскажите о себе',
        required=False,
    )

    image = forms.ImageField(
        required=False,
        label=u'Ваша фотография',
    )

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form'}),
        min_length=6,
        label=u'Старый пароль',
        error_messages={'min_length': 'Пароль должен быть не менее 6 символов'},
        required=False,
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form'}),
        min_length=6,
        label=u'Новый пароль',
        error_messages={'min_length': 'Пароль должен быть не менее 6 символов'},
        required=False,
    )

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=6,
        label=u'Повторите пароль',
        error_messages={'min_length': 'Пароль должен быть не менее 6 символов'},
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.cleaned_data['email'] != self.old_email:
            try:
                Traveler.objects.get(email=email)
                raise forms.ValidationError(u'Данная почта уже зарегистрирована!')
            except Traveler.DoesNotExist:
                pass
        return email

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if old_password and self.data['new_password'] and self.data['repeat_password']:
            try:
                user = authenticate(username=self.username, password=old_password)
                if not user.is_active:
                    raise forms.ValidationError(u'Старый пароль указан неверно')
            except:
                raise forms.ValidationError(u'Старый пароль указан неверно')
            pass1 = self.data['new_password']
            pass2 = self.data['repeat_password']
            if pass1 != pass2:
                raise forms.ValidationError(u'Пароли не совпадают')
        return old_password
