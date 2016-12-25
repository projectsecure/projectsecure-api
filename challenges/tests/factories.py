import factory
from challenges.models import Challenge
from faker import Factory as FakeFactory
from users.tests.factories import UserFactory

fake = FakeFactory.create()


class ChallengeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Challenge

    user = factory.SubFactory(UserFactory)
    status = Challenge.NOT_STARTED
