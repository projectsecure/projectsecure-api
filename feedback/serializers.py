from rest_framework import serializers
from feedback.models import Feedback


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = ('text',)

