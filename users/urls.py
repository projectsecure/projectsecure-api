from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from users.views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

router = SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^auth/login$', obtain_jwt_token, name='auth-jwt-obtain'),
    url(r'^auth/refresh$', refresh_jwt_token, name='auth-jwt-refresh'),
    url(r'^auth/verify$', verify_jwt_token, name='auth-jwt-verify'),
]
