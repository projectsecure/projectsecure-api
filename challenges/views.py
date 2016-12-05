from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from challenges.serializers import ChallengeMetaSerializer, ChallengeSerializer
from challenges.models.challenge import Challenge
from rest_framework.views import APIView
from challenges.models import CHALLENGES
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from challenges.models.challenge import IN_PROGRESS


class ChallengeViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        user = self.request.user
        return Challenge.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        serializer = ChallengeMetaSerializer(instance=CHALLENGES, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def start(self, request, pk):
        challenge = dict(CHALLENGES)[pk]()
        challenge.user = request.user
        challenge.status = IN_PROGRESS
        challenge.save()

        serializer = ChallengeSerializer(instance=challenge)
        return Response(serializer.data)


class ChallengeStepViewSet(APIView):
    def get_queryset(self):
        user = self.request.user
        return Challenge.objects.filter(user=user)

    def post(self, request,  *args, **kwargs):
        user = self.request.user
        challenge = Challenge.objects.filter(user=user)

        steps = challenge.ChallengeMeta.steps

        challenge.on_input(request.data)

        serializer = ChallengeMetaSerializer(instance=steps, many=True)

        return Response(serializer.data)
