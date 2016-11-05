from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from challenges.tests.factories import ChallengeFactory, ChallengeStepFactory


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


class TestChallengeStepViewSet(APITestCase):
    def test_retrieve_challenge_steps_list(self):
        challenge_step = ChallengeStepFactory()
        response = self.client.get(reverse('challenges-step-list', kwargs={
            'parent_lookup_challenge_steps': str(challenge_step.challenge.id)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'etc': challenge_step.etc, 'id': str(challenge_step.id),
             'title': challenge_step.title}])

    def test_retrieve_challenge_step_list_challenge_not_found(self):
        response = self.client.get(reverse('challenges-step-list',
                                           kwargs={'parent_lookup_challenge_steps': 'random'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_retrieve_challenge_steps_list(self):
        challenge_step = ChallengeStepFactory()
        response = self.client.get(reverse('challenges-step-detail', kwargs={
            'parent_lookup_challenge_steps': str(challenge_step.challenge.id),
            'pk': str(challenge_step.id)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'etc': challenge_step.etc, 'id': str(challenge_step.id),
             'title': challenge_step.title})

    def test_retrieve_challenge_steps_detail_not_found(self):
        challenge = ChallengeFactory()
        response = self.client.get(reverse('challenges-step-detail',
                                           kwargs={'parent_lookup_challenge_steps': str(challenge.id),
                                                   'pk': 'random'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

# TODO: Test get nested
