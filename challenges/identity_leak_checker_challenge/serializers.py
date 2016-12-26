from rest_framework.serializers import ModelSerializer, SerializerMethodField
from challenges.serializers import ChallengeSerializerMixin
from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge


class IdentityLeakCheckerChallengeSerializer(ChallengeSerializerMixin, ModelSerializer):
    title = SerializerMethodField()
    description = SerializerMethodField()
    steps = SerializerMethodField()

    class Meta:
        model = IdentityLeakCheckerChallenge
        fields = ChallengeSerializerMixin.Meta.fields
