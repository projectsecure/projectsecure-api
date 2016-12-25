import factory
from challenges.models import Challenge
from users.tests.factories import UserFactory


class ChallengeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Challenge

    user = factory.SubFactory(UserFactory)
    status = Challenge.NOT_STARTED
