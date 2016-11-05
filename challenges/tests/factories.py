import factory
from challenges.models import Challenge, ChallengeStep
from faker import Factory as FakeFactory
from random import randint

fake = FakeFactory.create()


class ChallengeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Challenge

    title = factory.Sequence(lambda n: 'Challenge {0}'.format(n))
    description = fake.text()


class ChallengeStepFactory(factory.DjangoModelFactory):
    class Meta:
        model = ChallengeStep

    title = factory.Sequence(lambda n: 'Challenge Step {0}'.format(n))
    etc = randint(0, 20)
    challenge = factory.SubFactory(ChallengeFactory)
