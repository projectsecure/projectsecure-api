from django.test import TestCase
from django.core.urlresolvers import reverse


class TestFeedbackUrls(TestCase):
    def test_feedback_url(self):
        url = reverse('feedback')
        self.assertEqual(url, '/api/feedback')

