from django.test import TestCase
from challenges.registry import CHALLENGES
from challenges.helpers import get_challenge_serializer


class TestChallengeSerializers(TestCase):
    def test_serialize_one(self):
        for challenge_type in CHALLENGES:
            challenge = challenge_type[1]()

            serializer = get_challenge_serializer(challenge_type[0])(instance=challenge)
            data = serializer.data

            self.assertEqual(data.pop('title'), challenge.ChallengeMeta.title)
            self.assertEqual(data.pop('description'), challenge.ChallengeMeta.description)
            self.assertEqual(data.pop('status'), challenge.status)
            self.assertEqual(data.pop('message'), challenge.message)
            for step in data.pop('steps'):
                self.assertContains(step, 'name')
                self.assertContains(step, 'status')
                self.assertContains(step, 'type')
                self.assertContains(step, 'options')
            self.assertEqual(len(data), 0)
