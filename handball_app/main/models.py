from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    personal_informations = models.TextField()
    account_pref = models.CharField(max_length=100)

class TrainingSession(models.Model):
    session_title = models.CharField(max_length=100)
    exercise = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    session_time = models.CharField(max_length=100)
    session_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Multimedia(models.Model):
    content_title = models.CharField(max_length=100)
    content_description = models.TextField()
    content_type = models.CharField(max_length=50)
    exercice_type = models.CharField(max_length=50)
    theme = models.CharField(max_length=100)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SessionTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100)

