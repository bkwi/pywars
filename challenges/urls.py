from django.conf.urls import patterns, include, url

from .views import ChallengeList, ChallengeRun, ChallengeAdd

urlpatterns = [
    url(r'^list', ChallengeList.as_view(), name='list'),
    url(r'^add', ChallengeAdd.as_view(), name='add'),
    url(r'^run', ChallengeRun.as_view(), name='run'),
]
