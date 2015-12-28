from django.conf.urls import patterns, include, url

from .views import (ChallengeList, ChallengeAdd, ChallengeEdit,
                    ChallengeSolve, ChallengeSolutions, VoteOnSolution,
                    SolutionCommentAPI, RunCode)

urlpatterns = [
    url(r'^list', ChallengeList.as_view(), name='list'),
    url(r'^add', ChallengeAdd.as_view(), name='add'),
    url(r'^(?P<pk>\w{16})$', ChallengeSolve.as_view(), name='solve'),
    url(r'^(?P<pk>\w{16})/edit', ChallengeEdit.as_view(), name='edit'),
    url(r'^(?P<pk>\w{16})/solutions', ChallengeSolutions.as_view(),
        name='solutions'),
    url(r'^run-code', RunCode.as_view(), name='run_code'),
    url(r'^(?P<pk>\w{16})/vote', VoteOnSolution.as_view(),
        name='vote_on_solution'),
    url(r'^solution-comment', SolutionCommentAPI.as_view(),
        name='solution_comment'),
]
