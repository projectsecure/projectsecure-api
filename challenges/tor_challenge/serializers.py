from rest_framework.serializers import ModelSerializer, SerializerMethodField
from challenges.serializers import ChallengeSerializerMixin
from challenges.tor_challenge.models import TorChallenge


class TorChallengeSerializer(ChallengeSerializerMixin, ModelSerializer):
    title = SerializerMethodField()
    description = SerializerMethodField()
    steps = SerializerMethodField()

    class Meta:
        model = TorChallenge
        fields = ChallengeSerializerMixin.Meta.fields
