from django.test import TestCase
from challenges.serializers import CHALLENGE_SERIALIZERS


class TestChallengeSerializers(TestCase):
    def test_challenges_list_unique(self):
        serializers_list = list(CHALLENGE_SERIALIZERS)
        serializers_dict = dict(CHALLENGE_SERIALIZERS)

        self.assertEqual(len(serializers_list), len(serializers_dict.keys()),
                         msg='Two challenges are violating the unique identifier constraint')
