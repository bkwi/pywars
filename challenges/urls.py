from django.conf.urls import patterns, include, url

from .views import ChallengeList, ChallengeAdd, ChallengeDetails, ChallengeEdit

urlpatterns = [
    url(r'^list', ChallengeList.as_view(), name='list'),
    url(r'^add', ChallengeAdd.as_view(), name='add'),
    url(r'^(?P<pk>\w{16})/edit', ChallengeEdit.as_view(), name='edit'),
    url(r'^(?P<pk>\w{16})', ChallengeDetails.as_view(), name='details'),
]
