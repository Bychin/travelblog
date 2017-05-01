from django.db import models
from django.utils import timezone

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


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    #title = models.CharField(max_length=100, default="")
    title = models.TextField(default="")
    text = models.TextField(default="")
    image = models.ImageField(default=None)
    geom = PointField(default=None)

    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def __unicode__(self):
        return self.title

    @property
    def picture_url(self):
        return self.image.url

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
