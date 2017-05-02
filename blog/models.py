from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from djgeojson.fields import PointField


class PlaceSpot(models.Model):
    description = models.CharField(max_length=100)
    picture = models.ImageField()
    geom = PointField()

    def __unicode__(self):
        return self.title

    @property
    def picture_url(self):
        return self.picture.url


class Rating(models.Model):
    likes = models.IntegerField(
        verbose_name='Likes', default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_by')
    dislikes = models.IntegerField(
        verbose_name='Dislikes', default=0)
    disliked_by = models.ManyToManyField(User, related_name='disliked_by')

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
    image = models.ImageField(blank=True, null=True)
    geom = PointField(blank=True)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    rating = models.OneToOneField(Rating, blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        rating = Rating()
        rating.save()
        self.rating = rating
        self.save()

    def add_comment(self, author, text):
        comment = Comment()
        comment.author = author
        comment.text = text
        comment.publish(self)
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def picture_url(self):
        return self.image.url


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    published_date = models.DateTimeField(
        blank=True, null=True)
    post = models.ForeignKey(Post, blank=True, null=True)

    def publish(self, post, reply_to=""):
        if reply_to != "":
            self.text = f"@{reply_to}\n{self.text}\n"
        self.published_date = timezone.now()
        self.post = post
        self.save()