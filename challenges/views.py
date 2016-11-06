from rest_framework.viewsets import ReadOnlyModelViewSet
from challenges.serializers import ChallengeSerializer, ChallengeStepSerializer
from challenges.models import Challenge, ChallengeStep
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import detail_route


class ChallengeViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()
    permission_classes = (AllowAny,)


class ChallengeStepViewSet(ReadOnlyModelViewSet):
    serializer_class = ChallengeStepSerializer
    queryset = ChallengeStep.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def state(self, request):
        return Response({})
