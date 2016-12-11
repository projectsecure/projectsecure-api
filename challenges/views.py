from rest_framework.viewsets import mixins, GenericViewSet
from challenges.serializers import CHALLENGE_SERIALIZERS
from rest_framework.permissions import AllowAny
from challenges.models import CHALLENGES
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from challenges.models import Challenge
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound


def get_challenge(name):
    challenge = dict(CHALLENGES).get(name, None)
    if challenge is None:
        raise NotFound
    return challenge


def get_challenge_serializer(name):
    """
    Returns a serialzer object based on a challenge name.

    Raises: NotFound - Error if callenge name was not found

    Returns: ChallengeSerializer - A specialized serializer for a challenge
    """
    serializer = dict(CHALLENGE_SERIALIZERS).get(name, None)
    if serializer is None:
        raise NotFound
    return serializer


class ChallengeViewSet(mixins.RetrieveModelMixin,
                       GenericViewSet):
    def get_queryset(self):
        raise NotImplementedError

    def retrieve(self, request, pk, *args, **kwargs):
        challenge = get_challenge(pk).objects.get(user=request.user)
        serializer = get_challenge_serializer(pk)(instance=challenge)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def start(self, request, pk):
        challenge = get_challenge(pk)()
        challenge.user = request.user
        challenge.status = Challenge.IN_PROGRESS
        challenge.save()
        serializer = get_challenge_serializer(pk)(instance=challenge)
        return Response(serializer.data)


class ChallengesMetaView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        data = [{'slug': challenge[0], 'title': challenge[1].ChallengeMeta.title,
                 'description': challenge[1].ChallengeMeta.description} for challenge in CHALLENGES]
        return Response(data)


class ChallengeStepViewSet(GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    def get_queryset(self):
        raise NotImplementedError

    def list(self, request, parent_lookup_challenge_steps, *args, **kwargs):
        steps = get_challenge(parent_lookup_challenge_steps).ChallengeMeta.steps
        data = [{'name': step[0], 'type': type(step[1]).__name__, 'options': step[1].to_json()} for
                step in steps]
        return Response(data)

    def update(self, request, parent_lookup_challenge_steps, pk, *args, **kwargs):
        challenge = get_challenge(parent_lookup_challenge_steps).objects.get(user=request.user)
        data = challenge.on_input(pk, request) or {}
        return Response(data)
