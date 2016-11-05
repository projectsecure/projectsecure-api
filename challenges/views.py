from rest_framework.viewsets import ReadOnlyModelViewSet
from challenges.serializers import ChallengeSerializer, ChallengeStepSerializer
from challenges.models import Challenge, ChallengeStep
from rest_framework.permissions import AllowAny


class ChallengeViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()
    permission_classes = (AllowAny,)


class ChallengeStepViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeStepSerializer
    queryset = ChallengeStep.objects.all()
    permission_classes = (AllowAny,)
