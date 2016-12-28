from django.test import TestCase
from users.tests.factories import UserFactory
from users.serializers import UserSerializer
from users.models import User


class TestUserSerializer(TestCase):
    def test_serialize_one(self):
        """
        Tests that the serializer properly deserializes a user
        """
        user = UserFactory()
        data = UserSerializer(user).data
        keys = {'username', 'color', 'email'}

        self.assertEqual(data.keys(), keys)
        self.assertEqual(data.pop('username'), user.username)
        self.assertEqual(data.pop('color'), user.color)
        self.assertEqual(data.pop('email'), user.email)

        self.assertEqual(len(data), 0)

    def test_create(self):
        """
        Tests that a user gets created when the serializer is initialized with valid data
        """
        data = {'username': 'ausername2348353', 'password': 'fsfsanbshfbsjkf', 'color': '#ffffff'}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, data['username'])
