from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge
from challenges.identity_leak_checker_challenge.serializers import IdentityLeakCheckerChallengeSerializer
from challenges.identity_leak_checker_challenge.tests.test_models import IdentityLeakCheckerChallengeFactory
from challenges.tor_challenge.models import TorChallenge
from challenges.tor_challenge.serializers import TorChallengeSerializer
from challenges.tor_challenge.tests.test_models import TorChallengeFactory

IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker'
TOR_CHALLENGE = 'tor'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge)
)

CHALLENGE_SERIALIZERS = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeSerializer),
    (TOR_CHALLENGE, TorChallengeSerializer)
)

CHALLENGE_FACTORIES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeFactory),
    (TOR_CHALLENGE, TorChallengeFactory)
)

