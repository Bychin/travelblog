from django.contrib.auth import authenticate
from django import forms
from .models import Traveler


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


class PostForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': "form-control"}),
        label=u'Название поста',
        max_length=100
    )

    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'class': 'form-control'}),
        label=u'Текст поста'
    )

    places_count = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    latitude1 = forms.FloatField(
        widget=forms.HiddenInput(),
    )
    longitude1 = forms.FloatField(
        widget=forms.HiddenInput(),
    )
    latitude2 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude2 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude3 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude3 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude4 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude4 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude5 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude5 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude6 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude6 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude7 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude7 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude8 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude8 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude9 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude9 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    latitude10 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    longitude10 = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    img = forms.ImageField(
        required=True,
        label=u'Изображение'
    )

    def save(self, post):
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.img = self.cleaned_data['img']
        places = []
        for i in range(self.cleaned_data['places_count']):
            places.append([self.cleaned_data['latitude' + str(i + 1)], self.cleaned_data['longitude' + str(i + 1)]])
        post.places = places
        post.save()
        return post


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
