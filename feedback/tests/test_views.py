from rest_framework.test import APITestCase
from feedback.models import Feedback
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from users.tests.factories import UserFactory
from django.core.urlresolvers import reverse


class TestSendFeedbackView(APITestCase):
    def test_send_feedback_authorized(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        text = 'test'

        response = self.client.post(reverse('feedback'), data={'text': text})
        feedback = Feedback.objects.first()

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {})
        self.assertEqual(feedback.text, text)
        self.assertEqual(feedback.user, user)

    def test_send_feedback_not_authorized(self):
        text = 'test'

        response = self.client.post(reverse('feedback'), data={'text': text})
        feedback = Feedback.objects.first()

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {})
        self.assertEqual(feedback.text, text)
        self.assertIsNone(feedback.user)

    def test_send_feedback_invalid_data(self):
        response = self.client.post(reverse('feedback'))

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'error': None, 'text': ['This field is required.']})
