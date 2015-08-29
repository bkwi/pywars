from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import DashboardView, IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
)
