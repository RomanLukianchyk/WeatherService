from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    webhook_url = models.URLField(null=True, blank=True)
