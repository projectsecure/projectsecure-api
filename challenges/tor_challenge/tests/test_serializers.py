from django.test import TestCase
from challenges.tor_challenge.tests.factories import TorChallengeFactory
from challenges.tor_challenge.serializers import TorChallengeSerializer


class TestTorChallengeSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a user
        """
        challenge = TorChallengeFactory()
        serializer = TorChallengeSerializer(instance=challenge)
        data = serializer.data

        self.assertEqual(data.pop('status'), challenge.status)
        self.assertEqual(data.pop('message'), challenge.message)
        self.assertEqual(data.pop('check_tor_connection_status'),
                         challenge.check_tor_connection_status)
        self.assertEqual(data.pop('meta'), serializer.get_meta(challenge))

        self.assertEqual(len(data), 0)
