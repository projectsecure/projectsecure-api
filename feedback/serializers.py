from rest_framework import serializers
from feedback.models import Feedback


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feedback
        fields = ('text',)

    def create(self, validated_data):
        obj = Feedback.objects.create(**validated_data)
        obj.user = self.context['request'].user
        obj.save()
        return obj

