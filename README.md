# Backend
|  Master | Develop   |
|---------|-----------|
|  [![Build Status](https://travis-ci.org/projectsecure/projectsecure-api.svg?branch=master)](https://travis-ci.org/projectsecure/projectsecure-api) | [![Build Status](https://travis-ci.org/projectsecure/projectsecure-api.svg?branch=develop)](https://travis-ci.org/projectsecure/projectsecure-api) |

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
- Email unique/required
- PEP8 testing
