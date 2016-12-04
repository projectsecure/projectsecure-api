from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from challenges.tests.factories import ChallengeFactory
from users.tests.factories import UserFactory


class TestChallengeViewSet(APITestCase):
    def test_retrieve_challenge(self):
        challenge = ChallengeFactory()
        response = self.client.get(reverse('challenge-detail', kwargs={'pk': challenge.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
            {'description': challenge.description, 'id': str(challenge.id),
             'title': challenge.title})

    def test_retrieve_challenge_not_found(self):
        pk = 'a_random_id'
        response = self.client.get(reverse('challenge-detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_retrieve_all_challenges(self):
        challenge = ChallengeFactory()
        response = self.client.get(reverse('challenge-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'description': challenge.description, 'id': str(challenge.id),
             'title': challenge.title}])


class TestChallengeOverviewView(APITestCase):
    def test_overview(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('challenge-overview'))
        print(response.json())
        raise NotImplementedError
