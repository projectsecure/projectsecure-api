from django.db import models
import uuid
from django.conf import settings
from challenges.exceptions import NotCompletedError, AlreadyCompletedError


class Challenge(models.Model):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

    STATUS_CHOICES = (
        (NOT_STARTED, 'Not started'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
        (ERROR, 'Error'),
    )

    class Meta:
        abstract = True

    class ChallengeMeta:
        title = None
        description = None
        steps = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NOT_STARTED)
    message = models.CharField(max_length=140, blank=True, null=False)

    def get_registered_steps_handlers(self):
        """
        Gets all methods that are registered through the register_step_handler decorator.
        """
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

    def on_input(self, step_name, request):
        step_func = self.get_registered_steps_handlers()[step_name]
        step_func(request)
        self.save()

    def mark_as_completed(self, raise_exception=False):
        """
        Marks a challenge as completed if all fields ending with _status are also completed
        """
        # Challenge can be only completed once
        if self.status == Challenge.COMPLETED:
            if raise_exception:
                raise AlreadyCompletedError
            return True

        fields = [field for field in self._meta.get_fields() if field.name.endswith('_status')]

        for completion_field in fields:
            # Look if the field is set to COMPLETED
            if getattr(self, completion_field.name) == Challenge.COMPLETED:
                continue

            # We may want to raise an exception in case the function should be used without nesting
            if raise_exception:
                raise NotCompletedError

            # Return False if first status field occurs without value of COMPLETED
            return False

        # Actually mark the challenge itself as completed
        self.status = Challenge.COMPLETED
        return True


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

