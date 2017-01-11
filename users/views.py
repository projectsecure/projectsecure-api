from rest_framework import viewsets
from rest_framework.decorators import list_route
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_204_NO_CONTENT
from users.models import User


class UserViewSet(viewsets.GenericViewSet, viewsets.DestroyModelMixin):
    queryset = User.objects.all()
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

    def destroy(self, request):
        request.user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
