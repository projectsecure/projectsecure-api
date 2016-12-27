from rest_framework.exceptions import NotFound
from challenges.registry import CHALLENGES
import re


def get_challenge(name) -> type:
    challenge = dict(CHALLENGES).get(name, None)
    if challenge is None:
        raise NotFound
    return challenge


def make_underscore(name) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
