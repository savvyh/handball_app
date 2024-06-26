from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = [
    ('mini_hand', 'Mini Hand'),
    ('-9', '-9'),
    ('-11F', '-11F'),
    ('-11G', '-11G'),
    ('-13F', '-13F'),
    ('-13G', '-13G'),
    ('-15F', '-15F'),
    ('-15G', '-15G'),
    ('-18F', '-18F'),
    ('-18G', '-18G'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, default='default_username')
    categories = models.ManyToManyField(Category)
    personal_informations = models.TextField(blank=True, null=True)
    account_pref = models.CharField(max_length=100, blank=True, null=True)

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

