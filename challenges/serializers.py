from rest_framework import serializers
from challenges.models.challenge import Challenge, ActionStep, TextStep, Step


class ChallengeMetaSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('slug', 'title', 'description')

    def get_title(self, obj):
        return obj[1].ChallengeMeta.title

    def get_description(self, obj):
        return obj[1].ChallengeMeta.description

    def get_slug(self, obj):
        return obj[0]


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('title', 'description', 'status', 'message')

    def get_title(self, obj):
        return obj.ChallengeMeta.title

    def get_description(self, obj):
        return obj.ChallengeMeta.description
