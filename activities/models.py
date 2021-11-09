from django.db import models

class Activity(models.Model):

    title = models.CharField(max_length=255, unique=True)
    points = models.FloatField()
