from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    color = models.CharField(max_length=7, validators=[
        RegexValidator(
            regex='^#(?:[0-9a-fA-F]{3}){1,2}$',
            message='Is not a valid color code',
        )
    ])
