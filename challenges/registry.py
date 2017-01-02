from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge
from challenges.identity_leak_checker_challenge.tests.test_models import \
    IdentityLeakCheckerChallengeFactory
from challenges.passphrase_challenge.models import PassphraseChallenge

from challenges.tor_challenge.models import TorChallenge
from challenges.tor_challenge.tests.test_models import TorChallengeFactory
from challenges.passphrase_challenge.tests.test_models import PassphraseChallengeFactory

IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker_challenge'
TOR_CHALLENGE = 'tor_challenge'
PASSPHRASE_CHALLENGE = 'passphrase_challenge'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge),
    (PASSPHRASE_CHALLENGE, PassphraseChallenge)
)

CHALLENGE_FACTORIES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeFactory),
    (TOR_CHALLENGE, TorChallengeFactory),
    (PASSPHRASE_CHALLENGE, PassphraseChallengeFactory)
)

