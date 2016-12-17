from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
	text = models.TextField()
	user = models.ForeignKey(User, null=True, blank=True)

