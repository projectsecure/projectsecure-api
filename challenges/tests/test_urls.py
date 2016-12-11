from django.test import TestCase
from django.core.urlresolvers import reverse


class TestChallengeUrls(TestCase):
    def test_challenge_list_url(self):
        url = reverse('challenge-list')
        self.assertEqual(url, '/api/challenges')

    def test_challenge_detail_url(self):
        pk = 'c35849a4-53ae-47e7-a559-3a32909693ed'
        url = reverse('challenge-detail', kwargs={'pk': pk})
        self.assertEqual(url, '/api/challenges/{0}'.format(pk))

    def test_challenge_start_url(self):
        pk = 'c35849a4-53ae-47e7-a559-3a32909693ed'
        url = reverse('challenge-start', kwargs={'pk': pk})
        self.assertEqual(url, '/api/challenges/{0}/start'.format(pk))


class TestChallengeStepUrls(TestCase):
    def test_challenge_step_list_url(self):
        parent = 'c35849a4-53ae-47e7-a559-3a32909693ed'
        url = reverse('challenges-step-list', kwargs={'parent_lookup_challenge_steps': parent})
        self.assertEqual(url, '/api/challenges/{0}/steps'.format(parent))

    def test_challenge_step_detail_url(self):
        parent = 'd35849a4-53ae-47e7-a559-3a32909693ed'
        pk = 'c35849a4-53ae-47e7-a559-3a32909693ed'
        url = reverse('challenges-step-detail',
                      kwargs={'parent_lookup_challenge_steps': parent, 'pk': pk})
        self.assertEqual(url, '/api/challenges/{0}/steps/{1}'.format(parent, pk))
