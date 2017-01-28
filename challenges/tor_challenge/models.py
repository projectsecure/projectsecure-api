import requests
from challenges.models import Challenge, TextStep, ButtonStep, register_step_handler
from django.db import models


class TorChallenge(Challenge):
    class ChallengeMeta:
        title = 'Anonym mit Tor surfen'
        summary = 'Lerne, wie du sicher und anonym mit dem Tor Browser normal und im "Deep Web" surfen kannst.'
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
        badge_path = ''

    check_tor_connection_status = models.CharField(max_length=11, choices=Challenge.STATUS_CHOICES,
                                                   default=Challenge.NOT_STARTED)

    @register_step_handler()
    def check_tor_connection(self, request):
        """
        Checks if the given IP is a Tor exit node

        Returns True if given IP is Tor exit node
        """
        if self.check_tor_connection_status == Challenge.COMPLETED:
            return

        ip = request.META.get('REMOTE_ADDR')
        url = 'https://check.torproject.org/exit-addresses'
        response = requests.get(url)

        if ip in (response.text or ''):
            self.check_tor_connection_status = Challenge.COMPLETED
        else:
            self.check_tor_connection_status = Challenge.ERROR


