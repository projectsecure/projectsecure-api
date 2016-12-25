from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge
from challenges.tests.factories import ChallengeFactory
from django.test import TestCase
from unittest.mock import patch, Mock, PropertyMock


class IdentityLeakCheckerChallengeFactory(ChallengeFactory):
    class Meta:
        model = IdentityLeakCheckerChallenge


class TestIdentityLeakCheckerChallenge(TestCase):
    def test_check_email(self):
        email = 'test@example.com'
        challenge = IdentityLeakCheckerChallengeFactory()
        url = 'https://sec.hpi.uni-potsdam.de/leak-checker/search'

        request_mock = Mock()
        request_mock.data.get.return_value = email

        with patch('requests.post') as patched_post:
            type(patched_post.return_value).ok = PropertyMock(return_value=True)

            challenge.check_email(request_mock)
            patched_post.assert_called_once_with(url, data={'email': email})
