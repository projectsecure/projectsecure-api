from rest_framework import serializers
from challenges.models import TorChallenge, IdentityLeakCheckerChallenge, IDENTITY_LEAK_CECKER_CHALLENGE, TOR_CHALLENGE


class ChallengeSerializerMixin:
    class Meta:
        fields = ('title', 'description', 'status', 'message')

    def get_title(self, obj):
        return obj.ChallengeMeta.title

    def get_description(self, obj):
        return obj.ChallengeMeta.description


class TorChallengeSerializer(serializers.HyperlinkedModelSerializer, ChallengeSerializerMixin):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = TorChallenge
        fields = ChallengeSerializerMixin.Meta.fields


class IdentityLeakCheckerChallengeSerializer(serializers.HyperlinkedModelSerializer,
                                             ChallengeSerializerMixin):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = IdentityLeakCheckerChallenge
        fields = ChallengeSerializerMixin.Meta.fields


CHALLENGE_SERIALIZERS = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallengeSerializer),
    (TOR_CHALLENGE, TorChallengeSerializer)
)
