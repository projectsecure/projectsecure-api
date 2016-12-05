from django.db import models
import uuid
from django.contrib.auth.models import User


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


class Challenge(models.Model):
    class ChallengeMeta:
        title = None
        description = None
        steps = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NOT_STARTED)
    message = models.CharField(max_length=140, blank=True, null=False)

    def get_registered_steps(self):
        registered_steps = {}
        for methodname in dir(self):
            attr = getattr(self, methodname)
            registered = getattr(attr, 'registered', False)

            if registered:
                registered_steps[methodname] = attr

        return registered_steps

    def on_input(self, key, *args, **kwargs):
        step_func = self.get_registered_steps()[key]
        step_func(args, kwargs)


def register_step(**kwargs):
    def decorator(func):
        func.registered = True
        return func
    return decorator


class Step:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def to_json(self):
        return {'title': self.title, 'text': self.text}


class TextStep(Step):
    pass


class ActionStep(Step):
    pass


