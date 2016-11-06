from django.db import models
import uuid
from django.contrib.auth.models import User


# Challenge
class Challenge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)


# Challenge Step
class ChallengeStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    etc = models.IntegerField(blank=False, null=False)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)


class TextChallengeStep(ChallengeStep):
    text = models.TextField()


class ActionChallengeStep(ChallengeStep):
    action_title = models.CharField(max_length=30, blank=False, null=False)


class TextInputChallengeStep(ChallengeStep):
    action_title = models.CharField(max_length=30, blank=False, null=False)
    input_title = models.CharField(max_length=30, blank=False, null=False)


# Challenge Step State
class ChallengeStepState(models.Model):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ERROR = "ERROR"

    STATUS_CHOICES = (
        (NOT_STARTED, 'Not started'),
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
        (ERROR, 'Error'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge_step = models.ForeignKey(ChallengeStep, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NOT_STARTED)
    message = models.CharField(max_length=140, blank=True, null=False)

    class Meta:
        unique_together = ('challenge_step', 'user',) # TODO: test


class ActionChallengeStepState(ChallengeStepState):
    pass


class TextInputChallengeStepState(ChallengeStepState):
    text_input = models.CharField(max_length=100, blank=False, null=False)
