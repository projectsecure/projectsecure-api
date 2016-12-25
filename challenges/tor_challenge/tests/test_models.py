from challenges.tor_challenge.models import TorChallenge
from challenges.tests.factories import ChallengeFactory
from django.test import TestCase
from unittest.mock import patch, Mock, PropertyMock


class TorChallengeFactory(ChallengeFactory):
    class Meta:
        model = TorChallenge


class TestTorChallenge(TestCase):
    def test_check_tor_connection(self):
        challenge = TorChallengeFactory()
        mocked_ip = '192.168.178.22'
        url = 'https://check.torproject.org/exit-addresses'

        request_mock = Mock()
        request_mock.META.get.return_value = mocked_ip

        with patch('requests.get') as patched_get:
            type(patched_get.return_value).text = PropertyMock(return_value=mocked_ip)

            challenge.check_tor_connection(request_mock)
            request_mock.META.get.assert_called_once_with('REMOTE_ADDR')
            patched_get.assert_called_once_with(url)
