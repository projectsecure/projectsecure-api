from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from challenges.tests.factories import ChallengeFactory, TorChallengeFactory
from users.tests.factories import UserFactory
from challenges.models import TOR_CHALLENGE


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


class TestTorChallenge(APITestCase):
    def test_start_challenge(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('challenge-start', kwargs={'pk': TOR_CHALLENGE}))

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    def test_start_challenge_already_started(self):
        pass

    def test_start_not_authorized(self):
        pass


class TestChallengeStepView(APITestCase):
    def test_list_challenge_steps(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('challenges-step-list',
                                           kwargs={'parent_lookup_challenge_steps': TOR_CHALLENGE}))

        assert False

    def test_detail_challenge_steps(self):
        tor_challenge = TorChallengeFactory()

        self.client.force_authenticate(user=tor_challenge.user)

        response = self.client.put(reverse('challenges-step-detail',
                                           kwargs={'parent_lookup_challenge_steps': TOR_CHALLENGE, 'pk': 'check_tor_connection'}))

        assert False
