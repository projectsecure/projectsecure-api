from django.test import TestCase
from django.core.urlresolvers import reverse


class TestChallengeUrls(TestCase):
    def test_challenge_list_url(self):
        url = reverse('challenge-list')
        self.assertEqual(url, '/api/challenges')

    def test_challenge_detail_url(self):
        challenge_name = 'a_challenge'
        url = reverse('challenge-detail', kwargs={'challenge_name': challenge_name})
        self.assertEqual(url, '/api/challenges/{0}'.format(challenge_name))

    def test_challenge_start_url(self):
        challenge_name = 'a_challenge'
        url = reverse('challenge-start', kwargs={'challenge_name': challenge_name})
        self.assertEqual(url, '/api/challenges/{0}/start'.format(challenge_name))

    def test_challenge_complete_url(self):
        challenge_name = 'a_challenge'
        url = reverse('challenge-complete', kwargs={'challenge_name': challenge_name})
        self.assertEqual(url, '/api/challenges/{0}/complete'.format(challenge_name))


class TestChallengeStepUrls(TestCase):
    def test_challenge_step_list_url(self):
        challenge_name = 'a_challenge'
        url = reverse('challenges-step-list', kwargs={'challenge_name': challenge_name})
        self.assertEqual(url, '/api/challenges/{0}/steps'.format(challenge_name))

    def test_challenge_step_detail_url(self):
        challenge_name = 'a_challenge'
        step_name = 'a_step'
        url = reverse('challenges-step-update',
                      kwargs={'challenge_name': challenge_name, 'step_name': step_name})
        self.assertEqual(url, '/api/challenges/{0}/steps/{1}'.format(challenge_name, step_name))
