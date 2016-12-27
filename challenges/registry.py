from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge
from challenges.identity_leak_checker_challenge.tests.test_models import \
    IdentityLeakCheckerChallengeFactory
from challenges.tor_challenge.models import TorChallenge
from challenges.tor_challenge.tests.test_models import TorChallengeFactory

IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker_challenge'
TOR_CHALLENGE = 'tor_challenge'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge)
)

CHALLENGE_FACTORIES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeFactory),
    (TOR_CHALLENGE, TorChallengeFactory)
)

