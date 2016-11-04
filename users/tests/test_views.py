from rest_framework.test import APITestCase
from faker import Factory as FakeFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from .factories import UserFactory, DEFAULT_PASSWORD
import datetime

fake = FakeFactory.create()


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
    def test_me(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse('user-me'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'username': user.username, 'last_name': user.last_name,
                                           'first_name': user.first_name})


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
        print(response.json())
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
