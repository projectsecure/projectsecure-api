from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from challenges.tests.factories import ChallengeFactory, TorChallengeFactory
from users.tests.factories import UserFactory
from challenges.models import TOR_CHALLENGE, CHALLENGES


class TestChallengeViewSet(APITestCase):
    def test_retrieve_challenge(self):
        challenge = TorChallengeFactory()
        response = self.client.get(reverse('challenge-detail', kwargs={'pk': TOR_CHALLENGE}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'description': challenge.ChallengeMeta.description,
                          'title': challenge.ChallengeMeta.title, 'status': challenge.status,
                          'message': challenge.message})

    def test_retrieve_challenge_not_found(self):
        pk = 'a_random_id'
        response = self.client.get(reverse('challenge-detail', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_retrieve_all_challenges(self):
        response = self.client.get(reverse('challenge-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{'title': challenge[1].ChallengeMeta.title,
                           'description': challenge[1].ChallengeMeta.description,
                           'slug': challenge[0]} for challenge in CHALLENGES])


class TestTorChallenge(APITestCase):
    def test_start_challenge(self):
        challenge = TorChallengeFactory()
        self.client.force_authenticate(user=challenge.user)

        response = self.client.post(reverse('challenge-start', kwargs={'pk': TOR_CHALLENGE}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'title': challenge.ChallengeMeta.title,
                                           'description': challenge.ChallengeMeta.description,
                                           'message': challenge.message,
                                           'status': challenge.status})

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
