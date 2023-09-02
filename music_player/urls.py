"""music_player URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('redirect/',views.redirect_page, name='redirect'),
    path('getuserprofile/', views.get_user_profile,name='get_user_profile'),
    path('genre_recommendations/', views.get_genre_recommendations,name='get_genre_recommendations'),
    path('admin/', admin.site.urls, name='admin'),
]
