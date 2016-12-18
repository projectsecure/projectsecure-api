from rest_framework import viewsets
from rest_framework.decorators import list_route
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['get'])
    def me(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data)

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

