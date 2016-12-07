from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, mixins, GenericViewSet
from challenges.serializers import ChallengeMetaSerializer, ChallengeSerializer
from challenges.models.challenge import Challenge
from rest_framework.permissions import AllowAny
from challenges.models import CHALLENGES
from rest_framework.response import Response
from rest_framework.decorators import detail_route, permission_classes
from challenges.models.challenge import IN_PROGRESS
from rest_framework.views import APIView


class ChallengeViewSet(mixins.RetrieveModelMixin,
                       GenericViewSet):
    def get_queryset(self):
        raise NotImplementedError

    def retrieve(self, request, pk, *args, **kwargs):
        challenge = dict(CHALLENGES)[pk].object.get(user=request.user)
        serializer = ChallengeSerializer(instance=challenge)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def start(self, request, pk):
        challenge = dict(CHALLENGES)[pk]()
        challenge.user = request.user
        challenge.status = IN_PROGRESS
        challenge.save()
        serializer = ChallengeSerializer(instance=challenge)
        return Response(serializer.data)


class ChallengesMetaView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        serializer = ChallengeMetaSerializer(instance=CHALLENGES, many=True)
        return Response(serializer.data)


class ChallengeStepViewSet(GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    def get_queryset(self):
        raise NotImplementedError

    def list(self, request, parent_lookup_challenge_steps, *args, **kwargs):
        steps = dict(CHALLENGES)[parent_lookup_challenge_steps].ChallengeMeta.steps

        data = [{'name': step[0], 'type': type(step[1]).__name__, 'options': step[1].to_json()} for
                step in steps]

        return Response(data)

    def update(self, request, parent_lookup_challenge_steps, pk, *args, **kwargs):
        challenge = dict(CHALLENGES)[parent_lookup_challenge_steps].objects.get(user=request.user)
        print(pk)
        data = challenge.on_input(pk, request) or {}

        return Response(data)
