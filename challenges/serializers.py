class ChallengeSerializerMixin:
    class Meta:
        fields = ('meta', 'status', 'message')

    def get_meta(self, obj):
        return {
            'title': obj.ChallengeMeta.title,
            'description': obj.ChallengeMeta.description,
            'steps': [{'name': step[0], 'type': type(step[1]), 'options': step.to_json()} for step
                      in obj.ChallengeMeta.steps]
        }
