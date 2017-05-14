from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json


class Traveler(User):
    about = models.TextField(default="")
    avatar = models.ImageField(default=None)
    notifications = models.TextField(default="")
    notification_count = models.IntegerField(default=0)

    def add_notification(self, notice):
        if self.notifications != "":
            arr = json.loads(self.notifications)
            arr.push(notice)
        else:
            arr = [notice]
        self.notifications = json.dumps(arr)
        self.notification_count += 1
        self.save()

    def check_notification(self, num):
        if num < self.notification_count:
            arr = json.loads(self.notifications)
            notice = arr.pop(num)
            self.notifications = json.dumps(arr)
            return notice
        else:
            return None

    def get_notifications(self):
        if self.notification_count == 0:
            return "No new notifications :c"
        else:
            return json.loads()


class Rating(models.Model):
    likes = models.IntegerField(
        verbose_name='Likes', default=0)
    liked_by = models.ManyToManyField(Traveler, related_name='liked_by')
    dislikes = models.IntegerField(
        verbose_name='Dislikes', default=0)
    disliked_by = models.ManyToManyField(Traveler, related_name='disliked_by')

    def add_like(self, user):
        if self.liked_by.filter(id=user.id).exists():
            self.liked_by.remove(user)
            self.likes -= 1
            return
        if self.disliked_by.filter(id=user.id).exists():
            self.disliked_by.remove(user)
            self.dislikes -= 1
        self.liked_by.add(user)
        self.likes += 1
        self.save()

    def add_dislike(self, user):
        if self.disliked_by.filter(id=user.id).exists():
            self.disliked_by.remove(user)
            self.dislikes -= 1
            return
        if self.liked_by.filter(id=user.id).exists():
            self.liked_by.remove(user)
            self.likes -= 1
        self.disliked_by.add(user)
        self.dislikes += 1
        self.save()


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    rating = models.OneToOneField(Rating, blank=True, null=True)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    img = models.ImageField(default=None)

    def publish(self):
        rating = Rating()
        rating.save()
        self.rating = rating
        self.published_date = timezone.now()
        self.save()

    def add_comment(self, author, text):
        comment = Comment()
        comment.author = author
        comment.text = text
        comment.publish(self)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def picture_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    published_date = models.DateTimeField(
        blank=True, null=True)
    post = models.ForeignKey(Post, blank=True, null=True)
    rating = models.OneToOneField(Rating, blank=True, null=True)

    def publish(self, post, reply_to=""):
        if reply_to != "":
            try:
                Traveler.objects.get(username=reply_to)
            except Traveler.DoesNotExist:
                return "There is no such user to reply :c"
            self.text = f"@{reply_to}\n{self.text}"
        self.published_date = timezone.now()
        self.post = post
        self.save()