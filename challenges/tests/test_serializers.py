from django.test import TestCase
from challenges.registry import CHALLENGES
from challenges.serializers import ChallengeSerializer


class TestChallengeSerializers(TestCase):
    def test_serialize_one(self):
        for challenge_type in CHALLENGES:
            challenge = challenge_type[1]()

            serializer = ChallengeSerializer(instance=challenge)
            data = serializer.data

            self.assertEqual(data.pop('title'), challenge.ChallengeMeta.title)
            self.assertEqual(data.pop('description'), challenge.ChallengeMeta.description)
            self.assertEqual(data.pop('status'), challenge.status)
            self.assertEqual(data.pop('message'), challenge.message)
            self.assertEqual(data.pop('slug'), challenge_type[0],
                             msg='The underscore class name should be equal to the slug hash.')
            for step in data.pop('steps'):
                keys = step.keys()
                self.assertIn('name', keys)
                self.assertIn('status', keys)
                self.assertIn('type', keys)
                self.assertIn('options', keys)
            self.assertEqual(len(data), 0)
