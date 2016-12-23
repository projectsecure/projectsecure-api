from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from users.tests.factories import UserFactory, DEFAULT_PASSWORD
import datetime


def create_token(user_obj, expired=False):
    from rest_framework_jwt.settings import api_settings
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user_obj)
    if expired:
        payload['exp'] = datetime.datetime.utcnow() - datetime.timedelta(seconds=300)
    token = jwt_encode_handler(payload)
    return token


class TestUserViewSet(APITestCase):
    def test_me_authenticated(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-me'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'username': user.username, 'full_name': user.full_name,
                                           'color': user.color, 'email': user.email})

    def test_me_unauthenticated(self):
        response = self.client.get(reverse('user-me'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'error': 'Authentication credentials were not provided.'})

    def test_register_user_with_valid_data(self):
        data = {
            'username': 'anewuser',
            'password': '1randompassword',
            'email': 'anewuser@test.de',
            'full_name': 'Peter Parker',
            'color': '#ffffff'
        }
        response = self.client.post(reverse('user-register'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data.pop('password')
        self.assertEqual(response.json(), data)

    def test_register_user_with_existing_data(self):
        user = UserFactory()
        data = {
            'username': user.username,
            'password': '1randompassword',
            'email': user.email,
            'color': user.color,
            'full_name': user.full_name
        }
        response = self.client.post(reverse('user-register'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'username': ['A user with that username already exists.']})

    def test_register_user_with_missing_data(self):
        data = {}
        response = self.client.post(reverse('user-register'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'color': ['This field is required.'],
                                           'full_name': ['This field is required.'],
                                           'password': ['This field is required.'],
                                           'username': ['This field is required.']})


class TestAuthObtainJWTView(APITestCase):
    def test_login_with_credentials(self):
        user = UserFactory()
        data = {'username': user.username, 'password': DEFAULT_PASSWORD}
        response = self.client.post(reverse('auth-jwt-obtain'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get('token') is not None)

    def test_login_with_wrong_credentials(self):
        data = {'username': 'atotallyrandomusernmae', 'password': 'atotallyrandompassword'}
        response = self.client.post(reverse('auth-jwt-obtain'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Unable to login with provided credentials.']})


class TestAuthRefreshJWTView(APITestCase):
    def test_refresh_with_valid_token(self):
        user = UserFactory()
        token = create_token(user)
        data = {'token': token}
        response = self.client.post(reverse('auth-jwt-refresh'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get('token') is not None)

    def test_refresh_with_invalid_token(self):
        data = {'token': 'sdfanfajnfsnfd'}
        response = self.client.post(reverse('auth-jwt-refresh'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Error decoding signature.']})


class TestAuthVerifyJWTView(APITestCase):
    def test_verify_with_valid_token(self):
        user = UserFactory()
        token = create_token(user)
        data = {'token': token}
        response = self.client.post(reverse('auth-jwt-verify'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'token': token})

    def test_verify_with_invalid_token(self):
        data = {'token': 'sdfanfajnfsnfd'}
        response = self.client.post(reverse('auth-jwt-verify'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Error decoding signature.']})

    def test_verify_with_expired_token(self):
        user = UserFactory()
        token = create_token(user, expired=True)
        data = {'token': token}
        response = self.client.post(reverse('auth-jwt-verify'), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Signature has expired.']})
