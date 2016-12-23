from challenges.models import Challenge


def convenience_complete(challenge):
    completion_fields = [field for field in challenge._meta.get_fields() if
                         field.name.endswith('_status')]
    assert len(completion_fields) > 0

    for completion_field in completion_fields:
        setattr(challenge, completion_field.name, Challenge.COMPLETED)
    challenge.save()
