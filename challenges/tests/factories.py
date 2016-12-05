import factory
from challenges.models.challenge import Challenge
from challenges.models.tor_challenge import TorChallenge
from faker import Factory as FakeFactory
from users.tests.factories import UserFactory

fake = FakeFactory.create()


class ChallengeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Challenge

    user = factory.SubFactory(UserFactory)


class TorChallengeFactory(ChallengeFactory):
    class Meta:
        model = TorChallenge
