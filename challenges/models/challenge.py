from django.db import models
import uuid
from django.contrib.auth.models import User


class Challenge(models.Model):
    class ChallengeMeta:
        title = None
        description = None
        steps = []

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NOT_STARTED)
    message = models.CharField(max_length=140, blank=True, null=False)

    step_map = {}

    def on_input(self, step_key, *args, **kwargs):
        step_function = self.step_map[step_key]
        step_function(args, kwargs)


class Step:
    def __init__(self, title, text):
        self.title = title
        self.text = text


class TextStep(Step):
    pass


class ActionStep(Step):
    def __init__(self, action_name):
        self.action_name = action_name

