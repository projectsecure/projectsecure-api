from challenges.models.challenge import Challenge, TextStep, ActionStep
import requests


class TorChallenge(Challenge):
    class ChallengeMeta:
        title = 'Anonym mit Tor surfen'
        description = """Mit dem HPI Identity Leak Checker können Sie mithilfe Ihrer E-Mailadresse
        prüfen, ob Ihre persönlichen Identitätsdaten bereits im Internet veröffentlicht wurden.
        Per Datenabgleich wird kontrolliert, ob Ihre E-Mailadresse in Verbindung mit anderen
        persönlichen Daten (z.B. Telefonnummer, Geburtsdatum oder Adresse) im Internet offengelegt
        wurde und missbraucht werden könnte."""
        steps = [
            ('introduction', TextStep(text='Starte die Challenge mit einem Klick auf den Button')),
            ('start_action', ActionStep(action_name='Start'))
        ]

    @staticmethod
    def check_tor_connection(ip):
        """
        Checks if the given IP is a Tor exit node

        Returns True if given IP is Tor exit node
        """
        url = 'https://check.torproject.org/exit-addresses'
        response = requests.get(url)
        return ip in (response.content or '')
