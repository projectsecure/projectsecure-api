from rest_framework import serializers
from challenges.serializers import ChallengeSerializerMixin
from challenges.identity_leak_checker_challenge.models import IdentityLeakCheckerChallenge


class IdentityLeakCheckerChallengeSerializer(serializers.HyperlinkedModelSerializer,
                                             ChallengeSerializerMixin):
    meta = serializers.SerializerMethodField()

    class Meta:
        model = IdentityLeakCheckerChallenge
        fields = ChallengeSerializerMixin.Meta.fields + ('check_email_status',)
