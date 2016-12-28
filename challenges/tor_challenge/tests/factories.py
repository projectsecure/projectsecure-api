from challenges.tor_challenge.models import TorChallenge
from challenges.tests.factories import ChallengeFactory


class TorChallengeFactory(ChallengeFactory):
    class Meta:
        model = TorChallenge
