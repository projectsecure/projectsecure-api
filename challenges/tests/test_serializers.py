from django.test import TestCase
from challenges.tests.factories import ChallengeFactory
from challenges.serializers import ChallengeMetaSerializer


class TestChallengeMetaSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge
        """
        challenge = ChallengeFactory()
        data = ChallengeMetaSerializer(challenge).data
        keys = {'title', 'description'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('title'), challenge.title)
        self.assertEqual(data.pop('description'), challenge.description)

        self.assertEqual(len(data), 0)

