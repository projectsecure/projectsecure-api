from django.test import TestCase
from django.core.urlresolvers import reverse


class TestUserUrls(TestCase):
    def test_me_url(self):
        url = reverse('user-me')
        self.assertEqual(url, '/api/users/me')

    def test_register_url(self):
        url = reverse('user-register')
        self.assertEqual(url, '/api/users/register')


class TestAuthUrls(TestCase):
    def test_login_url(self):
        url = reverse('auth-jwt-obtain')
        self.assertEqual(url, '/api/auth/login')

    def test_refresh_url(self):
        url = reverse('auth-jwt-refresh')
        self.assertEqual(url, '/api/auth/refresh')

    def test_verify_url(self):
        url = reverse('auth-jwt-verify')
        self.assertEqual(url, '/api/auth/verify')
