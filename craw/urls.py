"""craw URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^reviews/?$',views.tv_series_review,name="reviews"),
    url(r'^world-cup/?$',views.view_world_cup_expenses,name="world-cup"),
    url(r'^films-money/?$',views.films_money,name="films-money"),
    url(r'^world/?$',views.world,name="world"),
]
