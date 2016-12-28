from django.test import TestCase
from challenges.registry import CHALLENGES
from challenges.models import ButtonStep, Step, TextStep, InputStep, Challenge
from challenges.tests.helpers import convenience_complete
from challenges.tests.helpers import get_challenge_factory


class TestChallenge(TestCase):
    def test_challenges_list_unique(self):
        challenges_list = list(CHALLENGES)
        challenges_dict = dict(CHALLENGES)

        self.assertEqual(len(challenges_list), len(challenges_dict.keys()),
                         msg='Two challenges are violating the unique identifier constraint')

    def test_challenge_metas(self):
        for challenge_tuple in CHALLENGES:
            challenge = challenge_tuple[1]
            self.assertIsNotNone(challenge.ChallengeMeta.title,
                                 msg='{0} is missing a title'.format(challenge))
            self.assertIsNotNone(challenge.ChallengeMeta.description,
                                 msg='{0} is missing a description'.format(challenge))
            for step in challenge.ChallengeMeta.steps:
                self.assertEqual(type(step[0]), str)
                self.assertIn(type(step[1]), [ButtonStep, InputStep, TextStep],
                              msg='Steps in {0} needs have a given type'.format(challenge))

    def test_mark_as_completed(self):
        for challenge_tuple in CHALLENGES:
            challenge = get_challenge_factory(challenge_tuple[0])

            self.assertFalse(challenge.mark_as_completed())
            self.assertFalse(challenge.status == Challenge.COMPLETED)

            convenience_complete(challenge)

            self.assertTrue(challenge.mark_as_completed())
            self.assertTrue(challenge.status == Challenge.COMPLETED)

    def test_slug_equals_lowercase_class_name(self):
        for challenge_type in list(CHALLENGES):
            underscore_class_name = challenge_type[1]().underscore_type_name()
            print(underscore_class_name)
            print(challenge_type)
            self.assertEqual(challenge_type[0], underscore_class_name)


class TestStep(TestCase):
    def test_to_json(self):
        title = 'a random title'
        text = 'a random text'
        step = Step(title=title, text=text)

        self.assertEqual(step.to_json(), {'title': title, 'text': text})


class TestButtonStep(TestCase):
    def test_to_json(self):
        button_title = 'Click me'
        title = 'a random title'
        text = 'a random text'
        step = ButtonStep(button_title=button_title, title=title, text=text)

        self.assertEqual(step.to_json(),
                         {'title': title, 'text': text, 'button_title': button_title})


class TestTextStep(TestCase):
    def test_to_json(self):
        title = 'a random title'
        text = 'a random text'
        step = TextStep(title=title, text=text)

        self.assertEqual(step.to_json(), {'title': title, 'text': text})


class TestInputStep(TestCase):
    def test_to_json(self):
        button_title = 'Click me'
        input_title = 'this is a text field'
        title = 'a random title'
        text = 'a random text'
        step = InputStep(input_title=input_title, button_title=button_title, title=title, text=text)

        self.assertEqual(step.to_json(),
                         {'title': title, 'text': text, 'button_title': button_title,
                          'input_title': input_title})
