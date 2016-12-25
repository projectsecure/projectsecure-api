import requests
from challenges.models import Challenge, TextStep, InputStep, register_step_handler
from django.db import models


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

    check_email_status = models.CharField(max_length=11, choices=Challenge.STATUS_CHOICES,
                                          default=Challenge.NOT_STARTED)

    @register_step_handler()
    def check_email(self, request, *args, **kwargs):
        """
        Send the user's email to the HPI Identity Leak Checker

        Returns True if web request was successful
        """
        if self.check_email_status == Challenge.COMPLETED:
            return

        email = request.data.get('input')
        url = 'https://sec.hpi.uni-potsdam.de/leak-checker/search'
        response = requests.post(url, data={'email': email})

        if response.ok:
            self.check_email_status = Challenge.COMPLETED
        else:
            self.check_email_status = Challenge.ERROR
