from django.db import models
import uuid
from django.contrib.auth.models import User


class Challenge(models.Model):
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

    class Meta:
        abstract = True

    class ChallengeMeta:
        title = None
        description = None
        steps = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NOT_STARTED)
    message = models.CharField(max_length=140, blank=True, null=False)

    def get_registered_steps_handlers(self):
        registered_step_handlers = {}
        for methodname in dir(self):
            # Ignore all errors
            try:
                attr = getattr(self, methodname)
            except AttributeError:
                continue

            registered = getattr(attr, 'registered', False)

            if registered:
                registered_step_handlers[methodname] = attr

        return registered_step_handlers

    def on_input(self, key, request):
        step_func = self.get_registered_steps_handlers()[key]
        step_func(request)
        self.save()


def register_step_handler():
    def decorator(func):
        func.registered = True
        return func
    return decorator


class Step:
    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text

    def to_json(self):
        return {'title': self.title, 'text': self.text}


class TextStep(Step):
    pass


class ButtonStep(Step):
    def __init__(self, button_title: str, title: str, text: str=None):
        super(ButtonStep, self).__init__(title, text)
        self.button_title = button_title

    def to_json(self):
        json = super(ButtonStep, self).to_json()
        json.update({'button_title': self.button_title})
        return json


class InputStep(Step):
    def __init__(self, input_title: str, button_title: str, title: str, text: str = None):
        super(InputStep, self).__init__(title, text)
        self.input_title = input_title
        self.button_title = button_title

    def to_json(self):
        json = super(InputStep, self).to_json()
        json.update({'input_title': self.input_title, 'button_title': self.button_title})
        return json
