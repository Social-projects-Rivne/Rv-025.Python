"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from views.index_view import index
from views.login_view import login_view

urlpatterns = [
   url(r'^admin/', admin.site.urls),
   url(r'^index/', index, name='index'),
   url(r'^account/login/$', login_view, name='login'),
   url(r'^account/password_reset/$', auth_views.password_reset,
       name='password_reset'),
   url(r'^account/password_reset/done/$',
       auth_views.password_reset_done,
       name='password_reset_done'),
]
