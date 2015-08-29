from django.conf.urls import patterns, include, url

from .views import Challenge, ChallengeRun

urlpatterns = [
    url(r'^$', Challenge.as_view(), name='main'),
    url(r'^run', ChallengeRun.as_view(), name='run'),
]
