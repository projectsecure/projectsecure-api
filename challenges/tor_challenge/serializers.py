from rest_framework import serializers
from challenges.serializers import ChallengeSerializerMixin
from challenges.tor_challenge.models import TorChallenge


class TorChallengeSerializer(serializers.HyperlinkedModelSerializer, ChallengeSerializerMixin):
    meta = serializers.SerializerMethodField()

    class Meta:
        model = TorChallenge
        fields = ChallengeSerializerMixin.Meta.fields + ('check_tor_connection_status', )
