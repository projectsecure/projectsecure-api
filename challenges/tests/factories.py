import factory
from challenges.models import Challenge, ChallengeStep, ChallengeStepState, ActionChallengeStep, ActionChallengeStepState
from faker import Factory as FakeFactory
from random import randint
from users.tests.factories import UserFactory

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


class ChallengeStepStateFactory(factory.DjangoModelFactory):
    class Meta:
        model = ChallengeStepState

    user = factory.SubFactory(UserFactory)
    challenge_step = factory.SubFactory(ChallengeStepFactory)
    status = ChallengeStepState.NOT_STARTED
    message = "Not yet started" #TODO: Replace with fake


class ActionChallengeStepFactory(ChallengeStepFactory):
    class Meta:
        model = ActionChallengeStep

    action_title = fake.name()


class ActionChallengeStepStateFactory(ChallengeStepStateFactory):
    class Meta:
        model = ActionChallengeStepState

