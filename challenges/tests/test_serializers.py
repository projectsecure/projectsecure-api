from django.test import TestCase
from challenges.registry import CHALLENGE_SERIALIZERS


class TestChallengeSerializers(TestCase):
    def test_challenges_list_unique(self):
        serializers_list = list(CHALLENGE_SERIALIZERS)
        serializers_dict = dict(CHALLENGE_SERIALIZERS)

        self.assertEqual(len(serializers_list), len(serializers_dict.keys()),
                         msg='Two challenges are violating the unique identifier constraint')
# TODO: Test general serializers/ meta method!!!
