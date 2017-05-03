from django.test import TestCase
from django.http import HttpRequest
from .views import *


class PostTests(TestCase):
    def test_post_times(self):
        def fake_save(*args):
            pass

        Post.author = ''
        Post.save = fake_save

        post = Post()
        post.author = 'author'
        post.title = 'test'
        post.text = 'test'
        cur_time = timezone.now()

        self.assertGreaterEqual(cur_time, post.created_date, "post time test 1 - error")

        post.created_date = timezone.now()
        self.assertGreaterEqual(post.created_date, cur_time, "post time test 2 - error")

        post.publish()
        cur_time = timezone.now()
        self.assertGreaterEqual(cur_time, post.created_date, "post time test 3 - error")
        self.assertGreaterEqual(cur_time, post.published_date, "post time test 4 - error")


class ViewsTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.user = User()
        self.request.user.username = 'usr'

    def test_view_login(self):
        self.request.user.is_active = True
        self.assertEqual(str(my_login(self.request)),
                         str(redirect('/profile/usr/')), "views login test 1 - error")

        self.request.user.is_active = False
        self.request.method = 'POST'
        self.assertEqual(str(my_login(self.request)),
                         str(render(self.request, 'admin/login.html', {'form': LoginForm() })),
                         "views login test 2 - error")

        self.request.method = ''
        self.assertEqual(str(my_login(self.request)),
                         str(render(self.request, 'admin/login.html', {'form': LoginForm() })),
                         "views login test 3 - error")

    def test_view_post_new(self):
        self.assertEqual(str(post_new(self.request)),
                         str(render(self.request, 'admin/add_post.html', {'form': LoginForm()})),
                         "views post test 1 - error")

        self.request.method = 'POST'
        self.assertEqual(str(post_new(self.request)),
                         str(render(self.request, 'admin/add_post.html', {'form': LoginForm()})),
                         "views post test 2 - error")
