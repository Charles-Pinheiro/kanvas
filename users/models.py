from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    # username = models.CharField(max_length=255, unique=True)
    # password = models.CharField(max_length=255)
    # is_superuser = models.BooleanField()
    # is_staff = models.BooleanField()
