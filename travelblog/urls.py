from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from blog import views

urlpatterns = [
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$', auth_views.logout, {
        'template_name': 'admin\home.html'
    }, name='logout'),
    url(r'^signup/', include('register.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
    ]
