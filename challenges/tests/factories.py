import factory
from challenges.models import Challenge, TorChallenge, IdentityLeakCheckerChallenge, IDENTITY_LEAK_CECKER_CHALLENGE, TOR_CHALLENGE
from faker import Factory as FakeFactory
from users.tests.factories import UserFactory

fake = FakeFactory.create()


class ChallengeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Challenge

    user = factory.SubFactory(UserFactory)
    status = Challenge.NOT_STARTED


class TorChallengeFactory(ChallengeFactory):
    class Meta:
        model = TorChallenge


class IdentityLeakCheckerChallengeFactory(ChallengeFactory):
    class Meta:
        model = IdentityLeakCheckerChallenge


CHALLENGE_FACTORIES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeFactory),
    (TOR_CHALLENGE, TorChallengeFactory)
)


def get_challenge_factory(name) -> ChallengeFactory:
    return dict(CHALLENGE_FACTORIES)[name]()
