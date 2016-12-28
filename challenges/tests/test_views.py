from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from users.tests.factories import UserFactory
from challenges.models import Challenge
from django.db import transaction
from challenges.models import ButtonStep, InputStep
from challenges.registry import CHALLENGES
from challenges.tests.helpers import convenience_complete, get_challenge_factory
from challenges.serializers import ChallengeSerializer


class TestChallengeDetailView(APITestCase):
    def test_retrieve_challenge(self):
        for challenge_type in CHALLENGES:

            challenge = get_challenge_factory(challenge_type[0])

            self.client.force_authenticate(user=challenge.user)
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            serializer = ChallengeSerializer(instance=challenge)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), serializer.data)

    def test_retrieve_challenge_not_found(self):
        user = UserFactory()
        for challenge_type in CHALLENGES:
            self.client.force_authenticate(user=user)
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.json(), {'error': 'Not found.'})

    def test_retrieve_not_authorized(self):
        for challenge_type in CHALLENGES:
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(),
                         {'error': 'Authentication credentials were not provided.'})


class TestChallengesListView(APITestCase):
    def test_retrieve_all_challenges(self):
        user = UserFactory()

        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('challenge-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {})

    def test_retrieve_all_challenges_not_authorized(self):
        response = self.client.get(reverse('challenge-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'error': 'Authentication credentials were not provided.'})


class TestChallengeStepUpdateView(APITestCase):
    def test_update_step(self):
        # TODO, remove nesting level
        for challenge_type in CHALLENGES:
            challenge = get_challenge_factory(challenge_type[0])
            self.client.force_authenticate(user=challenge.user)

            for step_type in challenge.ChallengeMeta.steps:
                if type(step_type[1]) in [ButtonStep, InputStep]:
                    response = self.client.put(reverse('challenges-step-update',
                                                       kwargs={'challenge_name': challenge_type[0],
                                                               'step_name': step_type[0]}))
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    self.assertEqual(response.json(), {})

    def test_update_step_not_found(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        for challenge_type in CHALLENGES:
            for step_type in challenge_type[1].ChallengeMeta.steps:
                response = self.client.put(reverse('challenges-step-update',
                                                   kwargs={'challenge_name': challenge_type[0],
                                                           'step_name': step_type[0]}))

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                                 msg='Challenge should not be found for {0} type'.format(
                                     challenge_type[0]))
                self.assertEqual(response.json(), {'error': 'Not found.'})

    def test_update_step_not_authorized(self):
        for challenge_type in CHALLENGES:
            for step_type in challenge_type[1].ChallengeMeta.steps:
                response = self.client.put(
                    reverse('challenges-step-update', kwargs={'challenge_name': challenge_type[0],
                            'step_name': step_type[0]}))

                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertEqual(response.json(),
                                 {'error': 'Authentication credentials were not provided.'})


class TestChallengeStartView(APITestCase):
    def test_start_challenge(self):
        user = UserFactory()
        for challenge_type in CHALLENGES:
            self.client.force_authenticate(user=user)

            with transaction.atomic():
                response = self.client.post(
                    reverse('challenge-start', kwargs={'challenge_name': challenge_type[0]}))
            challenge = challenge_type[1].objects.first()
            serializer = ChallengeSerializer(instance=challenge)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), serializer.data)
            self.assertEqual(challenge.user, user)

    def test_start_challenge_already_started(self):
        for challenge_type in CHALLENGES:
            # Object already exits in database --> started
            challenge = get_challenge_factory(challenge_type[0])

            self.client.force_authenticate(user=challenge.user)

            with transaction.atomic():
                response = self.client.post(
                     reverse('challenge-start', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.json(), {'error': 'Challenge was already started.'})

    def test_start_not_authorized(self):
        for challenge_type in CHALLENGES:
            response = self.client.post(
                reverse('challenge-start', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(),
                             {'error': 'Authentication credentials were not provided.'})

    def test_challenge_not_found(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        challenge_name = 'a_name'

        response = self.client.post(reverse('challenge-start',
                                            kwargs={'challenge_name': challenge_name}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         msg='Challenge should not be found for {0} type'.format(challenge_name))
        self.assertEqual(response.json(), {'error': 'Not found.'})


class TestChallengeCompleteView(APITestCase):
    def test_complete_challenge(self):
        for challenge_type in CHALLENGES:
            challenge = get_challenge_factory(challenge_type[0])
            convenience_complete(challenge)

            self.client.force_authenticate(user=challenge.user)
            response = self.client.post(
                reverse('challenge-complete', kwargs={'challenge_name': challenge_type[0]}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), {})

    def test_complete_challenge_not_found_if_not_started(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        for challenge_type in CHALLENGES:
            response = self.client.post(
                reverse('challenge-complete', kwargs={'challenge_name': challenge_type[0]}))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.json(), {'error': 'Not found.'})

    def test_complete_challenge_not_authorized(self):
        for challenge_type in CHALLENGES:
            response = self.client.post(
                reverse('challenge-complete', kwargs={'challenge_name': challenge_type[0]}))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(),
                             {'error': 'Authentication credentials were not provided.'})

    def test_complete_challenge_not_all_steps_completed(self):
        for challenge_type in CHALLENGES:
            challenge = get_challenge_factory(challenge_type[0])

            self.client.force_authenticate(user=challenge.user)
            response = self.client.post(
                reverse('challenge-complete', kwargs={'challenge_name': challenge_type[0]}))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.json(), {'error': 'Not all steps completed.'})

    def test_complete_challenge_already_completed(self):
        for challenge_type in CHALLENGES:
            challenge = get_challenge_factory(challenge_type[0])
            challenge.status = Challenge.COMPLETED
            challenge.save()

            self.client.force_authenticate(user=challenge.user)
            response = self.client.post(
                reverse('challenge-complete', kwargs={'challenge_name': challenge_type[0]}))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.json(), {'error': 'Already completed.'})
