from django.test import TestCase
from challenges.identity_leak_checker_challenge.tests.factories import \
    IdentityLeakCheckerChallengeFactory
from challenges.identity_leak_checker_challenge.serializers import \
    IdentityLeakCheckerChallengeSerializer


class TestIdentityLeakCheckerChallengeSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a user
        """
        challenge = IdentityLeakCheckerChallengeFactory()
        serializer = IdentityLeakCheckerChallengeSerializer(instance=challenge)
        data = serializer.data

        self.assertEqual(data.pop('status'), challenge.status)
        self.assertEqual(data.pop('message'), challenge.message)
        self.assertEqual(data.pop('check_email_status'), challenge.check_email_status)
        self.assertEqual(data.pop('meta'), serializer.get_meta(challenge))

        self.assertEqual(len(data), 0)
