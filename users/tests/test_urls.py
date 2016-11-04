from django.test import TestCase
from django.core.urlresolvers import resolve


class UrlTestCase(TestCase):
    def test_login_url(self):
        resolver = resolve('/users/login/')
        assert resolver.view_name == 'rest_framework_jwt.views.ObtainJSONWebToken'

    def test_refresh_token_url(self):
        resolver = resolve('/users/refresh_token/')
        assert resolver.view_name == 'rest_framework_jwt.views.RefreshJSONWebToken'
