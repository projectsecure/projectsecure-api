from rest_framework import serializers
from challenges.models.challenge import Challenge


class ChallengeMetaSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('slug', 'title', 'description', 'steps')

    def get_title(self, obj):
        return obj[1].ChallengeMeta.title

    def get_description(self, obj):
        return obj[1].ChallengeMeta.description

    def get_slug(self, obj):
        return obj[0]

    def get_steps(self, obj):
        return obj[1].ChallengeMeta.steps


class ChallengeSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('title', 'description', 'steps', 'status', 'message')

    def get_steps(self, obj):
        return obj.ChallengeMeta.steps

    def get_title(self, obj):
        return obj.ChallengeMeta.title

    def get_description(self, obj):
        return obj.ChallengeMeta.description


class ChallengeStepSerializer(serializers.HyperlinkedModelSerializer):
    pass
    # TODO: Return format: {'type': 'action', 'options': {}}
