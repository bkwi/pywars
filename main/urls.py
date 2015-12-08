from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import (DashboardView, IndexView, FeedbackView, HallOfFame,
                    Notifications)
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # url(r'^$', IndexView.as_view(), name='index'),
    url(r'^$', RedirectView.as_view(pattern_name='user:login',
        permanent=True)),
    url(r'^feedback', FeedbackView.as_view(), name='feedback'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
    url(r'^hall-of-fame/', HallOfFame.as_view(), name='hall_of_fame'),
    url(r'^notifications', Notifications.as_view(), name='notifications'),
)
