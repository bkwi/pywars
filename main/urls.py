from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import DashboardView, IndexView
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # url(r'^$', IndexView.as_view(), name='index'),
    url(r'^$', RedirectView.as_view(pattern_name='user:login', permanent=True)),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
)
