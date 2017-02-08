import requests
from challenges.models import Challenge, TextStep, ButtonStep, register_step_handler
from django.db import models


class TorChallenge(Challenge):
    class ChallengeMeta:
        title = 'Anonym mit Tor surfen'
        summary = 'Lerne, wie du sicher und anonym mit dem Tor Browser normal und im "Deep Web" surfen kannst.'
        description = """Mit Tor kannst du anonym im Internet surfen ohne das deine Aktivität für andere sichtbar ist.
        Das funktioniert indem deine Verbindung über mehrere Computer geleitet wird die alle nur den direkten Vorgänger und direkten Nachfolger kennen.
        Somit weiß der Server, der deine Anfrage erhält, nicht von wem die Anfrage kommt.
        Doch vorsichtig! Du musst auch deine Surfgewohnheiten anpassen und darauf achten keine persönlichen Daten anzugeben,
        damit dich die Anonymität, die dir Tor bietet, schützt.
        Informiere dich hier, wie du den Tor Browser installieren kannst: https://www.torproject.org/download/download-easy.html.en"""
        steps = [
            ('introduction',
             TextStep(title='', text='Starte die Challenge mit einem Klick auf den Button')),
            ('check_tor_connection', ButtonStep(button_title='Prüfe Verbindung zu Tor', title=''))
        ]

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


