from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django import forms


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    img = models.FileField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'longitude', 'latitude', 'img']
        widgets = { 'title':forms.TextInput(attrs={'class': "form-control"}),
                    'text' : forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
                    'longitude' : forms.HiddenInput(),
                    'latitude' : forms.HiddenInput(),
                }
