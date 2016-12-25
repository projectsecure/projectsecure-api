from django.db import models
from django.conf import settings


class Feedback(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
