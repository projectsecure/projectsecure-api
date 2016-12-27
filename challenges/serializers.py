from challenges.models import Challenge
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from challenges.helpers import make_underscore


class ChallengeSerializer(ModelSerializer):
    title = SerializerMethodField()
    description = SerializerMethodField()
    steps = SerializerMethodField()
    slug = SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('title', 'description', 'status', 'message', 'steps', 'slug')

    def get_title(self, obj):
        return obj.ChallengeMeta.title

    def get_description(self, obj):
        return obj.ChallengeMeta.description

    def get_steps(self, obj):
        return [{'name': step[0],
                 'type': type(step[1]).__name__,
                 'status': obj.status_for_step(step[0]),
                 'options': step[1].to_json()} for step in
                obj.ChallengeMeta.steps]

    def get_slug(self, obj):
        class_name = type(obj).__name__
        return make_underscore(class_name)
