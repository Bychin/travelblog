from django.test import TestCase
from django.http import HttpRequest
from .views import *
from .forms import *


class ViewTests(TestCase):
    def test_views_register(self):
        request = HttpRequest()
        request.user = Traveler()
        request.user.username = 'usr'
        request.method = 'POST'
        self.assertEqual(str(register(request)),
                         str(redirect('/profile/usr/posts/')), "views register test 3 - error")


class FormsTest(TestCase):
    def setUp(self):
        self.form = SignupForm()

    def test_forms_signup_save(self):
        self.form.cleaned_data = {'username': 'usr', 'email': 'a@a.aa', 'password': 'pass', 'about': 'text'}
        new_user = self.form.save()
        self.assertEqual(new_user.username, 'usr', "forms signup test 1 - error")
        self.assertEqual(new_user.email, 'a@a.aa', "forms signup test 2 - error")
        self.assertEqual(new_user.is_active, True, "forms signup test 3 - error")
        self.assertEqual(new_user.is_superuser, False, "forms signup test 4 - error")
        self.assertNotEqual(new_user.password, 'pass', "forms signup test 5 - error")

    def test_forms_signup_clean_username(self):
        self.form.cleaned_data = {'username': 'usr', 'email': 'a@a.aa', 'password': 'pass', 'about': 'text'}
        self.form.save()

        error = False
        message = ''
        try:
            self.form.clean_username()
        except forms.ValidationError as e:
            error = True
            message = e.message
        self.assertTrue(error)
        self.assertEqual(message, 'Такой пользователь уже существует',
                         "forms clean username test 1 - error")

        self.form.cleaned_data['username'] = 'usr2'
        self.assertEqual(self.form.clean_username(), 'usr2', "forms clean username test 2 - error")

    def test_forms_signup_clean_email(self):
        self.form.cleaned_data = {'username': 'usr', 'email': 'a@a.aa', 'password': 'pass', 'about': 'text'}
        self.form.save()

        error = False
        message = ''
        try:
            self.form.clean_email()
        except forms.ValidationError as e:
            error = True
            message = e.message
        self.assertTrue(error)
        self.assertEqual(message, 'Данная почта уже зарегистрирована!',
                         "forms clean email test 1 - error")

        self.form.cleaned_data['email'] = 'b@a.aa'
        self.assertEqual(self.form.clean_email(), 'b@a.aa', "forms clean email test 2 - error")

    def test_forms_signup_clean_repeat_password(self):
        self.form.cleaned_data = {'username': 'usr', 'email': 'a@a.aa', 'password': 'pass',
                             'repeat_password': 'pass2', 'about': 'text'}
        self.form.save()
        error = False
        message = ''
        try:
            self.form.clean_repeat_password()
        except forms.ValidationError as e:
            error = True
            message = e.message
        self.assertTrue(error)
        self.assertEqual(message, 'Пароли не совпадают',
                         "forms clean password repeat test 1 - error")

        self.form.cleaned_data['repeat_password'] = 'pass'
        self.assertEqual(self.form.clean_repeat_password(), None,
                         "forms clean password repeat test 2 - error")