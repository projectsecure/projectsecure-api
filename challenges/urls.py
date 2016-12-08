from rest_framework_extensions.routers import ExtendedSimpleRouter
from challenges.views import ChallengeViewSet, ChallengeStepViewSet, ChallengesMetaView
from django.conf.urls import url, include

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'challenges', ChallengeViewSet, base_name='challenge')\
    .register(r'steps',
              ChallengeStepViewSet,
              base_name='challenges-step',
              parents_query_lookups=['challenge_steps'])

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^challenges$', ChallengesMetaView.as_view(), name='challenge-list'),
]
