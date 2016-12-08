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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    def __init__(self, title: str, text: str=None):
        self.title = title
        self.text = text

    def to_json(self):
        return {'title': self.title, 'text': self.text}


class TextStep(Step):
    pass


class ActionStep(Step):
    def __init__(self, action_title: str, title: str, text: str=None):
        super(ActionStep, self).__init__(title, text)
        self.action_title = action_title

    def to_json(self):
        return super(ActionStep, self).to_json().update({'action_title': self.action_title})


class IdentityLeakCheckerChallenge(Challenge):
    class ChallengeMeta:
        title = 'HPI Identity Leak Checker'
        description = """Mit dem HPI Identity Leak Checker können Sie mithilfe Ihrer E-Mailadresse
        prüfen, ob Ihre persönlichen Identitätsdaten bereits im Internet veröffentlicht wurden.
        Per Datenabgleich wird kontrolliert, ob Ihre E-Mailadresse in Verbindung mit anderen
        persönlichen Daten (z.B. Telefonnummer, Geburtsdatum oder Adresse) im Internet offengelegt
        wurde und missbraucht werden könnte."""
        steps = [
            ('introduction', TextStep(title='sdf', text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_mail', ActionStep(action_title='Check Mail', title='', text=''))
        ]

    @register_step_handler()
    def check_email(self, *args, **kwargs):
        """
        Send the user's email to the HPI Identity Leak Checker

        Returns True if web request was successful
        """
        email = self.user.email
        url = 'https://sec.hpi.uni-potsdam.de/leak-checker/search'
        response = requests.post(url, data={'email': email})
        return response.status_code == 200


class TorChallenge(Challenge):
    class ChallengeMeta:
        title = 'Anonym mit Tor surfen'
        description = """Mit dem HPI Identity Leak Checker können Sie mithilfe Ihrer E-Mailadresse
        prüfen, ob Ihre persönlichen Identitätsdaten bereits im Internet veröffentlicht wurden.
        Per Datenabgleich wird kontrolliert, ob Ihre E-Mailadresse in Verbindung mit anderen
        persönlichen Daten (z.B. Telefonnummer, Geburtsdatum oder Adresse) im Internet offengelegt
        wurde und missbraucht werden könnte."""
        steps = [
            ('introduction', TextStep(title='', text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_tor_connection', ActionStep(action_title='Check tor connection', title='', text=''))
        ]

    @register_step_handler()
    def check_tor_connection(self, request):
        """
        Checks if the given IP is a Tor exit node

        Returns True if given IP is Tor exit node
        """
        ip = request.META.get('REMOTE_ADDR')
        url = 'https://check.torproject.org/exit-addresses'
        response = requests.get(url)

        return ip in (response.text or '')


IDENTITY_LEAK_CECKER_CHALLENGE = 'identity_leak_checker'
TOR_CHALLENGE = 'tor'

CHALLENGES = (
    (IDENTITY_LEAK_CECKER_CHALLENGE, IdentityLeakCheckerChallenge),
    (TOR_CHALLENGE, TorChallenge)
)