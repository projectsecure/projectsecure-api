from rest_framework_extensions.routers import ExtendedSimpleRouter
from challenges.views import ChallengeViewSet, ChallengeMetaView
from django.conf.urls import url, include

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'challenges', ChallengeViewSet, base_name='challenge')

urlpatterns = [
    url(r'/challenges/meta', ChallengeMetaView.as_view(), name='challenge-meta'),
    url(r'^', include(router.urls)),
]
