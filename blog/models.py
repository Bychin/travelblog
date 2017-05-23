from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
import cent


class Traveler(User):
    about = models.TextField(default="")
    avatar = models.ImageField(upload_to='avatars', default=None, null=True, blank=True)
    notifications = models.TextField(default="", null=True, blank=True)
    notification_count = models.IntegerField(default=0, null=True, blank=True)

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

    @property
    def picture_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url


class Rating(models.Model):
    likes = models.IntegerField(
        verbose_name='Likes', default=0)
    liked_by = models.ManyToManyField(Traveler, related_name='liked_by')
    dislikes = models.IntegerField(
        verbose_name='Dislikes', default=0)
    disliked_by = models.ManyToManyField(Traveler, related_name='disliked_by')

    def push_likes(self):
        client = cent.Client("http://localhost:9000", "secret", timeout=1)
        try:
            client.publish("likes_updates", {
                "item": self.pk,
                "likes": self.likes,
                "dislikes": self.dislikes
            })
        except cent.CentException:
            pass

    def delete(self, **kwargs):
        super(Rating, self).delete(**kwargs)
        self.push_likes()

    def save(self, **kwargs):
        super(Rating, self).save(**kwargs)
        self.push_likes()

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
    places_count = models.IntegerField(default=0)
    longitude1 = models.FloatField(default=0)
    latitude1 = models.FloatField(default=0)
    longitude2 = models.FloatField(default=0, null=True, blank=True)
    latitude2 = models.FloatField(default=0, null=True, blank=True)
    longitude3 = models.FloatField(default=0, null=True, blank=True)
    latitude3 = models.FloatField(default=0, null=True, blank=True)
    longitude4 = models.FloatField(default=0, null=True, blank=True)
    latitude4 = models.FloatField(default=0, null=True, blank=True)
    longitude5 = models.FloatField(default=0, null=True, blank=True)
    latitude5 = models.FloatField(default=0, null=True, blank=True)
    longitude6 = models.FloatField(default=0, null=True, blank=True)
    latitude6 = models.FloatField(default=0, null=True, blank=True)
    longitude7 = models.FloatField(default=0, null=True, blank=True)
    latitude7 = models.FloatField(default=0, null=True, blank=True)
    longitude8 = models.FloatField(default=0, null=True, blank=True)
    latitude8 = models.FloatField(default=0, null=True, blank=True)
    longitude9 = models.FloatField(default=0, null=True, blank=True)
    latitude9 = models.FloatField(default=0, null=True, blank=True)
    longitude10 = models.FloatField(default=0, null=True, blank=True)
    latitude10 = models.FloatField(default=0, null=True, blank=True)
    places = models.TextField(default="", null=True, blank=True)
    img = models.ImageField(upload_to='posts', default=None)

    def publish(self):
        rating = Rating()
        rating.save()
        self.rating = rating
        self.published_date = timezone.now()
        places = []
        for i in range(self.places_count):
            places.append([getattr(self, "latitude"+str(i+1)), getattr(self, "longitude"+str(i+1))])
        self.places = places
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
        rating = Rating()
        rating.save()
        self.rating = rating
        self.save()
