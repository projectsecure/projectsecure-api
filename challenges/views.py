from challenges.serializers import CHALLENGE_SERIALIZERS
from rest_framework.permissions import AllowAny
from challenges.models import CHALLENGES
from rest_framework.response import Response
from challenges.models import Challenge
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.status import HTTP_409_CONFLICT


def get_challenge(name) -> 'Challenge':
    challenge = dict(CHALLENGES).get(name, None)
    if challenge is None:
        raise NotFound
    return challenge


def get_challenge_serializer(name):
    """
    Returns a serialzer object based on a challenge name.

    Raises: NotFound - Error if challenge name was not found

    Returns: ChallengeSerializer - A specialized serializer for a challenge
    """
    serializer = dict(CHALLENGE_SERIALIZERS).get(name, None)
    if serializer is None:
        raise NotFound
    return serializer


class ChallengeDetailView(APIView):
    def get(self, request, challenge_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        serializer = get_challenge_serializer(challenge_name)(instance=challenge)
        return Response(serializer.data)


class ChallengeStepsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, _, challenge_name):
        steps = get_challenge(challenge_name).ChallengeMeta.steps
        data = [{'name': step[0], 'type': type(step[1]).__name__, 'options': step[1].to_json()} for
                step in steps]
        return Response(data)


class ChallengeStepUpdateView(APIView):
    def put(self, request, challenge_name, step_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        data = challenge.on_input(step_name, request) or {}
        return Response(data)


class ChallengeStartView(APIView):
    def post(self, request, challenge_name):
        challenge = get_challenge(challenge_name)()
        challenge.user = request.user
        challenge.status = Challenge.IN_PROGRESS

        try:
            challenge.save()
        except IntegrityError:
            return Response({'error': 'Challenge was already started.'}, status=HTTP_409_CONFLICT)

        serializer = get_challenge_serializer(challenge_name)(instance=challenge)
        return Response(serializer.data)


class ChallengesListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, _):
        data = [{'slug': challenge[0], 'title': challenge[1].ChallengeMeta.title,
                 'description': challenge[1].ChallengeMeta.description} for challenge in CHALLENGES]
        return Response(data)


class ChallengeCompleteView(APIView):
    def post(self, request, challenge_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        challenge.mark_as_completed(raise_exception=True)
        serializer = get_challenge_serializer(challenge_name)(instance=challenge)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
