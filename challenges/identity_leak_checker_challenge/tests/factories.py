from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge
from challenges.tests.factories import ChallengeFactory


class IdentityLeakCheckerChallengeFactory(ChallengeFactory):
    class Meta:
        model = IdentityLeakCheckerChallenge

