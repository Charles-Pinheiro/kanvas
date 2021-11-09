from django.db import models

class Submission(models.Model):

    grade = models.FloatField()
    repo = models.CharField(max_length=255, unique=True)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='submissions')
    activity_id = models.ForeignKey('activities.Activity', on_delete=models.CASCADE, related_name='submissions')
