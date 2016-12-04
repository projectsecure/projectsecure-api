from django.test import TestCase
from challenges.models import CHALLENGES


class TestChallenge(TestCase):
    def test_challenges_list_unique(self):
        challenges_list = list(CHALLENGES)
        challenges_dict = dict(CHALLENGES)

        self.assertEqual(len(challenges_list), len(challenges_dict.keys()),
                         msg='Two challenges are violating the unique identifier constraint')
