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

## TODO
- Email confirmation
- Email uniquess/required
- PEP8 testing
