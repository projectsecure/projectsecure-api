from django.test import TestCase
from challenges.tests.factories import ChallengeFactory, ChallengeStepFactory, \
    ChallengeStepStateFactory, ActionChallengeStepStateFactory
from challenges.serializers import ChallengeSerializer, ChallengeStepSerializer, \
    ChallengeStepStateSerializer, ActionChallengeStepSerializer


class TestChallengeSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge
        """
        challenge = ChallengeFactory()
        data = ChallengeSerializer(challenge).data
        keys = {'id', 'title', 'description'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('id'), str(challenge.id))
        self.assertEqual(data.pop('title'), challenge.title)
        self.assertEqual(data.pop('description'), challenge.description)

        self.assertEqual(len(data), 0)


class TestChallengeStepSerializer(TestCase):
    class RequestMock:
        """
        Mocks a request object to be used in the context of a serializer
        """
        user = None

        def __init__(self, user):
            self.user = user

    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a challenge step
        """

        state = ChallengeStepStateFactory()
        user = state.user
        step = state.challenge_step
        request_mock = TestChallengeStepSerializer.RequestMock(user)

        data = ChallengeStepSerializer(step, context={'request': request_mock}).data
        keys = {'id', 'title', 'etc', 'state'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('id'), str(step.id))
        self.assertEqual(data.pop('title'), step.title)
        self.assertEqual(data.pop('etc'), step.etc)
        self.assertEqual(data.pop('state'), {'status': state.status, 'message': state.message})
        self.assertEqual(len(data), 0)

    def test_current_user_state(self):
        raise NotImplementedError


class TestActionChallengeStepSerializer(TestCase):
    def test_serialize_one(self):
        state = ActionChallengeStepStateFactory()
        user = state.user
        step = state.challenge_step
        request_mock = TestChallengeStepSerializer.RequestMock(user)

        data = ActionChallengeStepSerializer(step, context={'request': request_mock}).data
        keys = {'id', 'title', 'etc', 'state', 'type', 'action_title'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('id'), str(step.id))
        self.assertEqual(data.pop('title'), step.title)
        self.assertEqual(data.pop('type'), 'action')
        self.assertEqual(data.pop('action_title'), step.action_title)
        self.assertEqual(data.pop('state'), {'status': state.status, 'message': state.message})
        self.assertEqual(len(data), 0)


class TestChallengeStepStateSerializer(TestCase):
    def test_serialize_one(self):
        state = ChallengeStepStateFactory()
        data = ChallengeStepStateSerializer(state).data
        keys = {'status', 'message'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('status'), state.status)
        self.assertEqual(data.pop('message'), state.message)
        self.assertEqual(len(data), 0)
