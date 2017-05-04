from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from djgeojson.views import GeoJSONLayerView
from .models import Post


urlpatterns = [
    url(r'^profile/(?P<user_name>\w+)/?$', views.account, name='account'),
    url(r'^post/new/?$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/?$', views.post_detail, name='post_detail'),
    url(r'^$', views.home, name='home'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=Post, properties=('title', 'picture_url')), name='data')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
