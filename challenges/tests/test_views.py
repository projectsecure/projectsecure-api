from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from challenges.tests.factories import CHALLENGE_FACTORIES
from users.tests.factories import UserFactory
from challenges.models import TOR_CHALLENGE, CHALLENGES, Challenge


def get_challenge_factory(name):
    return dict(CHALLENGES)[name]


class TestChallengeDetailView(APITestCase):
    def test_retrieve_challenge(self):
        for challenge_type in CHALLENGES:

            challenge = get_challenge_factory(challenge_type[0])

            self.client.force_authenticate(user=challenge.user)
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(),
                         {'description': challenge.ChallengeMeta.description,
                          'title': challenge.ChallengeMeta.title, 'status': challenge.status,
                          'message': challenge.message})

    def test_retrieve_challenge_not_found(self):
        user = UserFactory()
        for challenge_type in CHALLENGES:
            self.client.force_authenticate(user=user)
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_retrieve_not_authorized(self):
        for challenge_type in CHALLENGES:
            response = self.client.get(
                reverse('challenge-detail', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(),
                         {'detail': 'Authentication credentials were not provided.'})


class TestChallengesListView(APITestCase):
    def test_retrieve_all_challenges(self):
        response = self.client.get(reverse('challenge-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{'title': challenge[1].ChallengeMeta.title,
                           'description': challenge[1].ChallengeMeta.description,
                           'slug': challenge[0]} for challenge in CHALLENGES])


class TestChallengeStepsView(APITestCase):
    def test_retrieve_all_steps(self):
        for challenge_type in CHALLENGES:
            response = self.client.get(reverse('challenges-step-list', kwargs={
                'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            expected_response = [{'name': step[0], 'type': type(step[1]).__name__,
                                  'options': step[1].to_json()} for step in
                                 challenge_type[1].ChallengeMeta.steps]
            self.assertEqual(response.json(), expected_response)


class TestChallengeStepUpdateView(APITestCase):
    def test_update_step(self):
        pass

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
                self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_update_step_not_authorized(self):
        for challenge_type in CHALLENGES:
            for step_type in challenge_type[1].ChallengeMeta.steps:
                response = self.client.put(
                    reverse('challenges-step-update', kwargs={'challenge_name': challenge_type[0],
                            'step_name': step_type[0]}))

                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertEqual(response.json(),
                         {'detail': 'Authentication credentials were not provided.'})


class TestChallengeStartView(APITestCase):
    def test_start_challenge(self):
        for challenge_type in CHALLENGES:
            challenge = get_challenge_factory(challenge_type[0])

            self.client.force_authenticate(user=challenge.user)

            response = self.client.post(reverse('challenge-start', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), {'title': challenge.ChallengeMeta.title,
                                               'description': challenge.ChallengeMeta.description,
                                               'message': challenge.message,
                                               'status': Challenge.IN_PROGRESS})

    def test_start_challenge_already_started(self):
        pass

    def test_start_not_authorized(self):
        for challenge_type in CHALLENGES:
            response = self.client.post(
                reverse('challenge-start', kwargs={'challenge_name': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.json(),
                             {'detail': 'Authentication credentials were not provided.'})

    def test_challenge_not_found(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        challenge_name = 'a_name'

        response = self.client.post(reverse('challenge-start',
                                            kwargs={'challenge_name': challenge_name}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         msg='Challenge should not be found for {0} type'.format(challenge_name))
        self.assertEqual(response.json(), {'detail': 'Not found.'})



"""

class TestChallengeStepView(APITestCase):
    def test_list_challenge_steps_not_found(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        for challenge_type in CHALLENGES:
            response = self.client.get(reverse('challenges-step-list',
                                           kwargs={'parent_lookup_challenge_steps': challenge_type[0]}))

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                             msg='Challenge should not be found for {0} type'.format(challenge_type[0]))
            self.assertEqual(response.json(), {})

    def test_list_challenge_steps(self):
        challenge = TorChallengeFactory()
        self.client.force_authenticate(user=challenge.user)



    def test_detail_challenge_steps(self):
        tor_challenge = TorChallengeFactory()

        self.client.force_authenticate(user=tor_challenge.user)

        response = self.client.put(reverse('challenges-step-detail',
                                           kwargs={'parent_lookup_challenge_steps': TOR_CHALLENGE,
                                                   'pk': 'check_tor_connection'}))

        assert False

"""
