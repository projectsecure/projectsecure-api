from django.test import TestCase
from challenges.tests.factories import ChallengeStepStateFactory
from django.db.utils import IntegrityError


class TestChallengeStepState(TestCase):
    def test_unique_constraint(self):
        state1 = ChallengeStepStateFactory()
        state2 = ChallengeStepStateFactory()

        state1.user = state2.user
        state1.challenge_step = state2.challenge_step

        with self.assertRaises(IntegrityError):
            state1.save()
