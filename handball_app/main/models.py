from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

CATEGORY_CHOICES = [
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

THEME_CHOICES = [
    ('Échauffement', 'ÉCHAUFFEMENT'),
    ('Motricité', 'MOTRICITÉ'),
    ('Attaque', 'ATTAQUE'),
    ('Défense', 'DÉFENSE'),
    ('Techniques', 'TECHNIQUES'),
    ('Spécifique', 'SPÉCIFIQUE'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    profile_limit = models.PositiveIntegerField(default=1)
    categories = models.ManyToManyField(Category, blank=True)
    personal_informations = models.TextField(blank=True, null=True)
    account_pref = models.CharField(max_length=100, blank=True, null=True)
    profile_completed = models.BooleanField(default=False)

    def can_add_profile(self):
        return self.profiles.count() < self.profile_limit

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class TrainingSession(models.Model):
    session_title = models.CharField(max_length=100)
    exercise = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    session_time = models.CharField(max_length=100)
    session_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Theme(models.Model):
    name = models.CharField(max_length=100, choices=THEME_CHOICES, default='Échauffement')

    def __str__(self):
        return self.name

class Exercise(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Multimedia(models.Model):
    title = models.CharField(max_length=100)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='multimedia', default=1)
    description = models.TextField()
    theme = models.ManyToManyField(Theme)
    categories = models.ManyToManyField(Category)
    video = models.FileField(upload_to='videos_uploaded', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    video_time = models.CharField(max_length=50, default='00:00:00')
    other_file = models.FileField(upload_to='files/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SessionTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100)