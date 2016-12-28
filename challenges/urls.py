from challenges.views import ChallengesListView, ChallengeDetailView, \
    ChallengeStepUpdateView, ChallengeStartView, ChallengeCompleteView, BadgesListView, \
    ChallengeBadgeView
from django.conf.urls import url

urlpatterns = [
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/steps/(?P<step_name>[a-z_]+)$',
        ChallengeStepUpdateView.as_view(), name='challenges-step-update'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/start$', ChallengeStartView.as_view(),
        name='challenge-start'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/complete$', ChallengeCompleteView.as_view(),
        name='challenge-complete'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)$', ChallengeDetailView.as_view(),
        name='challenge-detail'),
    url(r'^challenges/(?P<challenge_name>[a-z_]+)/badge$', ChallengeBadgeView.as_view(),
        name='challenge-detail'),
    url(r'^challenges$', ChallengesListView.as_view(), name='challenge-list'),
    url(r'^badges$', BadgesListView.as_view(), name='badge-list'),
]
