from django.test import TestCase
from unittest.mock import patch, Mock, PropertyMock
from challenges.passphrase_challenge.tests.factories import PassphraseChallengeFactory
from challenges.models import Challenge

class TestPassphraseChallenge(TestCase):
    def test_check_passphrase(self):
        def test_cases_for_status(cases, expected_status):
            for case in cases:
                challenge = PassphraseChallengeFactory()    # reset challenge status
                request_mock_valid = Mock()
                request_mock_valid.data.get.return_value = case
                challenge.check_passphrase(request_mock_valid)
                self.assertEqual(challenge.check_passphrase_status, expected_status)

        # test valid cases
        cases_valid = ["FischerFritzFischtFrischeFische42"]
        test_cases_for_status(cases_valid, Challenge.COMPLETED)

        # test invalid cases
        cases_invalid = [
            "FischerFritzFischtFrische42",
            "FischerFritzFischtFrischeFische",
            "fischerfritzfischtfrischefische42"
        ]
        test_cases_for_status(cases_invalid, Challenge.ERROR)
