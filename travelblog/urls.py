from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blog import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', auth_views.logout, {
        'template_name': 'admin/home.html'
    }, name='logout'),
    url(r'^signup/', include('register.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static('/favicon.ico', document_root='static/favicon.ico')

handler404 = 'blog.views.error_404'
