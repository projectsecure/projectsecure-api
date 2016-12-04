from challenges.models.challenge import Challenge, TextStep, ActionStep
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
            ('introduction', TextStep(text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_mail' , ActionStep(action_title='Start'))
        ]

    def __init__(self):
        super(IdentityLeakCheckerChallenge, self).__init__()

        self.step_map = {
            'check_mail': self.check_email
        }

    def check_email(self, *args, **kwargs):
        """
        Send the user's email to the HPI Identity Leak Checker

        Returns True if web request was successful
        """
        email = self.user.email
        url = 'https://sec.hpi.uni-potsdam.de/leak-checker/search'
        response = requests.post(url, data={'email': email})
        return response.status_code == 200
