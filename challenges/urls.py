from challenges.views import ChallengesListView, ChallengeDetailView, ChallengeStepsView, \
    ChallengeStepUpdateView, ChallengeStartView

from django.conf.urls import url

urlpatterns = [
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/steps/(?P<step_name>[a-z_]+)$',
        ChallengeStepUpdateView.as_view(), name='challenges-step-update'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/steps$', ChallengeStepsView.as_view(),
        name='challenges-step-list'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/start$', ChallengeStartView.as_view(),
        name='challenge-start'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)$', ChallengeDetailView.as_view(),
        name='challenge-detail'),
    url(r'^challenges$', ChallengesListView.as_view(), name='challenge-list'),
]
