from rest_framework.permissions import AllowAny
from challenges.registry import CHALLENGES
from rest_framework.response import Response
from challenges.models import Challenge
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from challenges.exceptions import AlreadyStartedError
from challenges.helpers import get_challenge
from challenges.serializers import ChallengeSerializer
from challenges.renderers import PNGRenderer
from django.conf import settings


class ChallengeDetailView(APIView):
    def get(self, request, challenge_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        serializer = ChallengeSerializer(instance=challenge)
        return Response(serializer.data)


class ChallengeStepUpdateView(APIView):
    def put(self, request, challenge_name, step_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        challenge.on_input(step_name, request)
        return Response({})


class ChallengeStartView(APIView):
    def post(self, request, challenge_name):
        challenge = get_challenge(challenge_name)()
        challenge.user = request.user
        challenge.status = Challenge.IN_PROGRESS

        try:
            challenge.save()
        except IntegrityError:
            raise AlreadyStartedError

        serializer = ChallengeSerializer(instance=challenge)
        return Response(serializer.data)


class ChallengesListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        # Get all possible challenges
        all_challenge_map = {k: v() for k, v in dict(CHALLENGES).items()}

        if request.user.is_authenticated():
            # Fetch all challenges that the user has in the db
            challenges_with_status = Challenge.objects.filter(user=request.user).all()

            # Replace challenges where the user has a status
            # O(n) vs O(n^2) when using list for both
            for challenge in challenges_with_status:
                challenge_name = challenge.underscore_type_name()
                all_challenge_map[challenge_name] = challenge

        # Put that back into a list for serializer
        challenges = all_challenge_map.values()
        serializer = ChallengeSerializer(instance=challenges, many=True)
        return Response(serializer.data)


class ChallengeCompleteView(APIView):
    def post(self, request, challenge_name):
        challenge_type = get_challenge(challenge_name)
        challenge = get_object_or_404(challenge_type, user=request.user)
        challenge.mark_as_completed(raise_exception=True)
        challenge.save()
        return Response({})


class BadgesListView(APIView):
    def get(self, _):
        pass


class ChallengeBadgeView(APIView):
    renderer_classes = (PNGRenderer, )
    permission_classes = (AllowAny, )

    def get(self, _, challenge_name):
        challenge_type = get_challenge(challenge_name)
        image_path = '{0}/challenges/{1}/static/img/badge_{1}.png'.format(settings.BASE_DIR,
                                                                          challenge_name)
        image = open(image_path, 'rb')
        return Response(data=image)

