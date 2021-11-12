from django.db import models

class Submission(models.Model):

    grade = models.FloatField(null=True)
    repo = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='submissions')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE, related_name='submissions')
