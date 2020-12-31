"""webwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from temp1 import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = {
    path(r'admin/', admin.site.urls),
    path(r'index', views.index),
    path(r'db_handle', views.db_handle),
    path('', views.search),
    path(r'letter_game', views.letter_game),
    path(r'letter_game/register', views.letter_game_register),
    path(r'letter_game/login', views.letter_game_login),
    url(r'^letter_game/play/([0-9a-zA-Z]+)$', views.letter_game_play),
    url(r'^letter_game/show/([0-9a-zA-Z]+)$', views.letter_game_show),

    # set(staticfiles_urlpatterns()),
}
