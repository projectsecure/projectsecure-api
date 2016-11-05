from rest_framework import serializers
from challenges.models import Challenge, ChallengeStep


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description')


class ChallengeStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChallengeStep
        fields = ('id', 'title', 'etc')


class ActionChallengeStepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChallengeStep
        fields = ('id', 'title', 'etc', 'action_title')
