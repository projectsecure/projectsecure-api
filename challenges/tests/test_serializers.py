from django.test import TestCase
from challenges.tests.factories import ChallengeFactory
from challenges.serializers import ChallengeMetaSerializer


class TestChallengeMetaSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge
        """
        challenge_slug = 'a_challenge'
        challenge = (challenge_slug, ChallengeFactory())
        data = ChallengeMetaSerializer(challenge).data
        keys = {'title', 'description', 'slug'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('title'), challenge[1].ChallengeMeta.title)
        self.assertEqual(data.pop('description'), challenge[1].ChallengeMeta.description)
        self.assertEqual(data.pop('slug'), challenge_slug)

        self.assertEqual(len(data), 0)

