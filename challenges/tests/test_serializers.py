from django.test import TestCase
from challenges.tests.factories import ChallengeFactory, ChallengeStepFactory
from challenges.serializers import ChallengeSerializer, ChallengeStepSerializer


class TestChallengeSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge
        """
        challenge = ChallengeFactory()
        data = ChallengeSerializer(challenge).data
        keys = {'id', 'title', 'description'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('id'), str(challenge.id))
        self.assertEqual(data.pop('title'), challenge.title)
        self.assertEqual(data.pop('description'), challenge.description)

        self.assertEqual(len(data), 0)


class TestChallengeStepSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge
        """
        challenge = ChallengeStepFactory()
        data = ChallengeStepSerializer(challenge).data
        keys = {'id', 'title', 'etc'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('id'), str(challenge.id))
        self.assertEqual(data.pop('title'), challenge.title)
        self.assertEqual(data.pop('etc'), challenge.etc)

        self.assertEqual(len(data), 0)
