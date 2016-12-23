# Backend
|  Master | Develop   |
|---------|-----------|
|  [![Build Status](https://travis-ci.org/projectsecure/backend.svg?branch=master)](https://travis-ci.org/projectsecure/backend) | [![Build Status](https://travis-ci.org/projectsecure/backend.svg?branch=develop)](https://travis-ci.org/projectsecure/backend) |

## Development
1. Install Docker and docker-compose
2. Changes are auto-reflected
2. Run `$ docker-machine ip default` to get IP of Docker machine

## Tests
```
$ docker-compose run web py.test
```

## How to add a new challenge
In `challenges.models.py` add a new challenge class that inherits from `Challenge`.

```python
class AnExampleChallenge(Challenge):
    class ChallengeMeta:
        title = 'This is the title'
        description = "This should be a long description text."
        steps = [
            ('introduction',
             TextStep(title='Introduction', text='This is an introduction text.')),
            ('a_button_step', ButtonStep(button_title='Test something', title=''))
        ]
```

Define a callback for the `a_button_step` step defined in `steps` above using the `register_step_handler()` decorator. You should also define a corresponding status field for each individual step.

```python
a_button_step_status = models.CharField(max_length=11, choices=Challenge.STATUS_CHOICES,
                                       default=Challenge.NOT_STARTED)

```

```python
@register_step_handler()
def a_button_step(self, request):
    # Return early if step is already completed
    if self.a_button_step_status == Challenge.COMPLETED:
        return

    # Do some calculations or checks

    if error_that_happened is not None:
        self.a_button_step_status == Challenge.ERROR
    else:
        self.a_button_step_status == Challenge.COMPLETED

```

If and only if all steps (so, their status fields) are marked as `COMPLETED`, the user can finish a challenge.

At last, register a slug under with the challenge should be reachable.

```python
AN_EXAMPLE_CHALLENGE = 'an_example_challenge'

CHALLENGES = (
    …
    (AN_EXAMPLE_CHALLENGE, AnExampleChallenge)
)
```

**Note**: Don't forget to add tests for specialized behaviour in `challenges/tests/tests_models.py`.

## TODO
- Email confirmation
- Email unique/required
- PEP8 testing
