from rest_framework.permissions import AllowAny
from challenges.registry import CHALLENGES
from rest_framework.response import Response
from challenges.models import Challenge
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from challenges.exceptions import AlreadyStartedError
from challenges.helpers import get_challenge, get_challenge_serializer


class ChallengeDetailView(APIView):
    def get(self, request, challenge_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        serializer = get_challenge_serializer(challenge_name)(instance=challenge)
        return Response(serializer.data)


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
            raise AlreadyStartedError

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
        challenge.save()
        return Response({})
