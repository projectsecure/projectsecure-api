from rest_framework.exceptions import NotFound
from challenges.registry import CHALLENGES


def get_challenge(name) -> type:
    challenge = dict(CHALLENGES).get(name, None)
    if challenge is None:
        raise NotFound
    return challenge
