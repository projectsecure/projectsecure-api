from django.test import TestCase
from challenges.registry import CHALLENGES
from challenges.helpers import make_underscore


class TestSlugs(TestCase):
    def test_slug_equals_lowercase_class_name(self):
        challenges = list(CHALLENGES)
        for challenge_type in challenges:
            underscore_class_name = make_underscore(challenge_type[1].__name__)
            self.assertEqual(challenge_type[0], underscore_class_name)
