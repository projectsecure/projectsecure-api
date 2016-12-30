from challenges.passphrase_challenge.models import PassphraseChallenge
from challenges.tests.factories import ChallengeFactory

class PassphraseChallengeFactory(ChallengeFactory):
    class Meta:
        model = PassphraseChallenge
