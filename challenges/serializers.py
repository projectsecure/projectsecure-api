from challenges.models import Challenge
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class ChallengeSerializer(ModelSerializer):
    title = SerializerMethodField()
    description = SerializerMethodField()
    steps = SerializerMethodField()
    slug = SerializerMethodField()
    summary = SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('title', 'summary', 'description', 'status', 'message', 'steps', 'slug')

    def get_title(self, obj):
        return obj.ChallengeMeta.title
    
    def get_summary(self, obj):
        return obj.ChallengeMeta.summary
    
    def get_description(self, obj):
        return obj.ChallengeMeta.description

    def get_steps(self, obj):
        return [{'name': step[0],
                 'type': type(step[1]).__name__,
                 'status': obj.status_for_step(step[0]),
                 'options': step[1].to_json()} for step in
                obj.ChallengeMeta.steps]

    def get_slug(self, obj):
        return obj.underscore_type_name()
