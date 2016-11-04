from rest_framework import viewsets
from rest_framework.decorators import list_route
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['get'], url_path='me')
    def me(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data)
