from django.db import models
import uuid
from django.contrib.auth.models import User
import requests


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


class IdentityLeakCheckerChallenge(Challenge):
    class ChallengeMeta:
        title = 'HPI Identity Leak Checker'
        description = """Mit dem HPI Identity Leak Checker können Sie mithilfe Ihrer E-Mailadresse
        prüfen, ob Ihre persönlichen Identitätsdaten bereits im Internet veröffentlicht wurden.
        Per Datenabgleich wird kontrolliert, ob Ihre E-Mailadresse in Verbindung mit anderen
        persönlichen Daten (z.B. Telefonnummer, Geburtsdatum oder Adresse) im Internet offengelegt
        wurde und missbraucht werden könnte."""
        steps = [
            ('introduction',
             TextStep(title='sdf', text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_email', InputStep(input_title='Enter email', button_title='Check', title=''))
        ]

    @register_step_handler()
    def check_email(self, request, *args, **kwargs):
        """
        Send the user's email to the HPI Identity Leak Checker

        Returns True if web request was successful
        """
        if self.status == Challenge.DONE:
            return

        email = request.data.get('input')
        url = 'https://sec.hpi.uni-potsdam.de/leak-checker/search'
        response = requests.post(url, data={'email': email})

        if response.ok:
            self.status = Challenge.DONE
        else:
            self.status = Challenge.ERROR


class TorChallenge(Challenge):
    class ChallengeMeta:
        title = 'Anonym mit Tor surfen'
        description = """Mit dem HPI Identity Leak Checker können Sie mithilfe Ihrer E-Mailadresse
        prüfen, ob Ihre persönlichen Identitätsdaten bereits im Internet veröffentlicht wurden.
        Per Datenabgleich wird kontrolliert, ob Ihre E-Mailadresse in Verbindung mit anderen
        persönlichen Daten (z.B. Telefonnummer, Geburtsdatum oder Adresse) im Internet offengelegt
        wurde und missbraucht werden könnte."""
        steps = [
            ('introduction',
             TextStep(title='', text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_tor_connection', ButtonStep(button_title='Check tor connection', title=''))
        ]

    @register_step_handler()
    def check_tor_connection(self, request):
        """
        Checks if the given IP is a Tor exit node

        Returns True if given IP is Tor exit node
        """
        if self.status == Challenge.DONE:
            return

        ip = request.META.get('REMOTE_ADDR')
        url = 'https://check.torproject.org/exit-addresses'
        response = requests.get(url)

        if ip in (response.text or ''):
            self.status = Challenge.DONE
        else:
            self.status = Challenge.ERROR


IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker'
TOR_CHALLENGE = 'tor'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge)
)
