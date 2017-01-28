# Backend
|  Master | Develop   |
|---------|-----------|
|  [![Build Status](https://travis-ci.org/projectsecure/projectsecure-api.svg?branch=master)](https://travis-ci.org/projectsecure/projectsecure-api) | [![Build Status](https://travis-ci.org/projectsecure/projectsecure-api.svg?branch=develop)](https://travis-ci.org/projectsecure/projectsecure-api) |

## Development
1. Install Docker and docker-compose
2. Run `$ docker-machine ip default` to get IP of Docker machine (mac only)
3. Run `$ docker-compose run web python3 manage.py migrate` to migrate database
4. Run `$ docker-compose run web python3 manage.py makemigrations` in case of model changes. Code changes get auto reflected due to the mounted volume
5. Access site on docker IP at port 80

## Tests
```
$ docker-compose run web py.test
```

## How to add a new challenge
Add a new challenge by creating a new package in `challenges` with the the following structure.
```
└── an_example_challenge
    ├── __init__.py
    ├── models.py
    ├── static
    │   └── img
    │       └── badge_an_example_challenge.png
    └── tests
        ├── __init__.py
        ├── factories.py
        └── test_models.py
```

In `models.py` add the new challenge that inherits from `Challenge`.

```python
from challenges.models import Challenge, TextStep, ButtonStep, register_step_handler
from django.db import models


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
a_button_step_message = models.CharField(max_length=200)
```

```python
@register_step_handler()
def a_button_step(self, request):
    # Return early if step is already completed
    if self.a_button_step_status == Challenge.COMPLETED:
        return

    # Do some calculations or checks

    if some_error is None: 
        self.a_button_step_status == Challenge.COMPLETED
        self.a_button_step_message == 'All done. Nice ;)'
    else:
        self.a_button_step_status == Challenge.ERROR
        self.a_button_step_message == 'Something happened. Try again.'        
```

If and only if all steps (so, their status fields) are marked as `COMPLETED`, the user can complete a challenge.

At last, register a slug in `challenges/registry.py` under with the challenge should be reachable.

```python
AN_EXAMPLE_CHALLENGE = 'an_example_challenge'

CHALLENGES = (
    …
    (AN_EXAMPLE_CHALLENGE, AnExampleChallenge)
)
```

**Note**: Don't forget to add tests for specialized behaviour in `challenges/tests/tests_models.py`.

