from rest_framework.test import APITestCase
from feedback.models import Feedback
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from users.tests.factories import UserFactory
from django.core.urlresolvers import reverse


class TestSendFeedbackView(APITestCase):
	def test_send_feedback_authorized(self):
		user = UserFactory()
		self.client.force_authenticate(user=user)
		text = 'test'

		response = self.client.post(reverse('feedback'), data={'text': text}) 
		feedback = Feedback.objects.first()
		
		print(response.content)
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		self.assertEqual(response.content, b'')
		self.assertEqual(feedback.text, text)
		self.assertEqual(feedback.user, user)
		
	def test_send_feedback_not_authorized(self):
		text = 'test'

		response = self.client.post(reverse('feedback'), data={'text': text}) 
		feedback = Feedback.objects.first()
		
		print(response.content)
		self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
		self.assertEqual(response.content, b'')
		self.assertEqual(feedback.text, text)
		self.assertIsNone(feedback.user)
		
	def test_send_feedback_invalid_data(self):
		response = self.client.post(reverse('feedback')) 
		
		print(response.content)
		self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
		self.assertEqual(response.json(), 
				{'error': None, 'text': ['This field is required.']})

