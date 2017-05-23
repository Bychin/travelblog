from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^settings/$', views.account_settings, name='account_settings'),
    url(r'^profile/(?P<user_name>\w+)/posts/page(?P<num>[0-9]+)/$', views.account_posts, name='account_posts'),
    url(r'^post/new/?$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^posts/page(?P<num>[0-9]+)/$', views.all_posts, name='all_posts'),
    url(r'^$', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
