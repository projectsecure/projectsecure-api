from challenges.models.identity_leak_challenge_checker import IdentityLeakCheckerChallenge
from challenges.models.tor_challenge import TorChallenge

IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker'
TOR_CHALLENGE = 'tor'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge)
)
