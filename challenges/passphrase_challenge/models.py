from challenges.models import Challenge, TextStep, InputStep, register_step_handler
from django.db import models

class PassphraseChallenge(Challenge):
    class ChallengeMeta:
        title = 'Passphrase statt Passwort'
        summary = """Die meisten Passwörter sind auf Grund ihrer Kürze oder geringen Komplexität sehr schwach.
            Passphrases bieten eine Lösung für dieses Problem. Eine Passphrase ist ein Passwort, das länger ist
            als die typischen acht bis zwanzig Zeichen und besteht häufig aus einem ganzen Satz statt -
            wie für Passwörter üblich - einem einzelnen Wort.
            """
        description = ("Die meisten Passwörter sind auf Grund ihrer Kürze oder geringen Komplexität sehr schwach."
            "**Passphrases** bieten eine Lösung für dieses Problem.\n\n"
            "Eine **Passphrase** ist ein Passwort, das länger ist als die typischen acht bis zwanzig Zeichen und"
            "besteht häufig aus einem ganzen Satz statt - wie für Passwörter üblich - einem einzelnen Wort.")
        steps = [
            ('introduction', TextStep(
                title="Kriterien für sichere Passphrases",
                text=("Eine gute **Passphrase** erhält man, indem man folgende Punkte beachtet:\n\n"
                      "* Mehr als 30 Zeichen\n"
                      "* Mindestens einen Großuchstaben\n"
                      "* Mindestens eine Zahl\n\n"
                      "**Beispiel:** FischerFritzFischtFrischeFische42")
            )),
            ('check_passphrase', InputStep(
                text=("Wenn du das Gefühl hast, dass du die Kriterien verstanden hast, dann gib hier eine **Passphrase**"
                    "ein, die dir sicher vorkommt, um dein neues Wissen zu überprüfen.\n\n"
                    "*Die eingegebene **Passphrase** wird nicht gespeichert.*"),
                input_title='Enter a passphrase',
                button_title='Check',
                title=''
            )),
        ]

    check_passphrase_status = models.CharField(
        max_length=11,
        choices=Challenge.STATUS_CHOICES,
        default=Challenge.NOT_STARTED
    )

    @register_step_handler()
    def check_passphrase(self, request):
        """
        Returns True if pass phrase is longer then min length
        """

        input = request.data.get('input')

        rules = [
            lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
            lambda s: any(x.islower() for x in s),  # must have at least one lowercase
            lambda s: any(x.isdigit() for x in s),  # must have at least one digit
            lambda s: len(s) >= 30  # must be at least 30 characters
        ]

        secure = all(rule(input) for rule in rules)

        if secure:
            self.check_passphrase_status = Challenge.COMPLETED
        else:
            self.check_passphrase_status = Challenge.ERROR


