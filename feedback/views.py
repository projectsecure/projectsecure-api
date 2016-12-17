from feedback.models import Feedback
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from feedback.serializers import FeedbackSerializer


class SendFeedbackView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request):
		serializer = FeedbackSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(status=HTTP_204_NO_CONTENT)
		
