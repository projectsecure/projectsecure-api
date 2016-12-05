from rest_framework_extensions.routers import ExtendedSimpleRouter
from challenges.views import ChallengeViewSet
from django.conf.urls import url, include

router = ExtendedSimpleRouter(trailing_slash=False)
router.register(r'challenges', ChallengeViewSet, base_name='challenge')

urlpatterns = [
    url(r'^', include(router.urls)),
]
