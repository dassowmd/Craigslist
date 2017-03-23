"""CraigslistAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListingCreateAPIView, ListingDeleteAPIView, ListingDetailAPIView, ListingListAPIView, ListingUpdateAPIView

urlpatterns = [
    url(r'^$', ListingListAPIView.as_view(), name='list'),
    url(r'^create/$', ListingCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>[\w-]+)/$', ListingDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w-]+)/edit/$', ListingUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', ListingDeleteAPIView.as_view(), name='delete'),
    ]
