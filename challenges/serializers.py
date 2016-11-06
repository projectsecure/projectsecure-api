from rest_framework import serializers
from challenges.models import Challenge, ChallengeStep, ChallengeStepState, ActionChallengeStep


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description')


class ChallengeStepStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChallengeStepState
        fields = ('status', 'message')


class ChallengeStepSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.SerializerMethodField('current_user_state')

    class Meta:
        model = ChallengeStep
        fields = ('id', 'title', 'etc', 'state')

    def current_user_state(self, obj):
        user = self.context['request'].user
        state = ChallengeStepState.objects.get(challenge_step=obj, user=user)
        serializer = ChallengeStepStateSerializer(state)
        return serializer.data


class ActionChallengeStepSerializer(ChallengeStepSerializer):
    class Meta:
        model = ActionChallengeStep
        fields = ChallengeStepSerializer.Meta.fields + ('type', 'action_title')
