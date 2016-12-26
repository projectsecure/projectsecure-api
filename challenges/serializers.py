class ChallengeSerializerMixin:
    class Meta:
        fields = ('title', 'description', 'status', 'message', 'steps')

    def get_title(self, obj):
        return obj.ChallengeMeta.title

    def get_description(self, obj):
        return obj.ChallengeMeta.description

    def get_steps(self, obj):
        return [{'name': step[0], 'type': type(step[1]).__name__,
                 'status': obj.status_for_step(step[0]), 'options': step[1].to_json()} for step in
                obj.ChallengeMeta.steps]
