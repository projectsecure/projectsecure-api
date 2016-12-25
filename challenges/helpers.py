from rest_framework.exceptions import NotFound
from challenges.registry import CHALLENGES, CHALLENGE_SERIALIZERS


def get_challenge(name) -> type:
    challenge = dict(CHALLENGES).get(name, None)
    if challenge is None:
        raise NotFound
    return challenge


def get_challenge_serializer(name) -> type:
    """
    Returns a serialzer object based on a challenge name.

    Raises: NotFound - Error if challenge name was not found

    Returns: ChallengeSerializer - A specialized serializer for a challenge
    """
    serializer = dict(CHALLENGE_SERIALIZERS).get(name, None)
    if serializer is None:
        raise NotFound
    return serializer
