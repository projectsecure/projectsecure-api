from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from challenges.serializers import ChallengeMetaSerializer, ChallengeSerializer
from challenges.models.challenge import Challenge
from rest_framework.views import APIView
from challenges.models import CHALLENGES
from rest_framework.response import Response


class ChallengeViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        user = self.request.user
        return Challenge.objects.filter(user=user)


class ChallengeMetaView(APIView):
    def get(self, *args, **kwargs):
        serializer = ChallengeMetaSerializer(instance=CHALLENGES, many=True)
        return Response(serializer.data)


class ChallengeStepViewSet(APIView):
    def get_queryset(self):
        user = self.request.user
        return Challenge.objects.filter(user=user)

    def post(self, *args, **kwargs):
        user = self.request.user
        challenge = Challenge.objects.filter(user=user)

        steps = challenge.ChallengeMeta.steps

        challenge.on_input()

        serializer = ChallengeMetaSerializer(instance=s, many=True)

        return Response(serializer.data)
