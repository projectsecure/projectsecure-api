from challenges.models.challenge import Challenge, register_step_handler, TextStep, InputStep
import requests


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


