from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

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

class Personalisation(models.Model):
    class Exercice(models.Model):
        title = models.CharField(max_length=100)
        label="Insérer un nouveau type d'exercice"

        def __str__(self):
            return self.title

    class Theme(models.Model):
        title = models.CharField(max_length=100)
        label="Insérer un nouveau thème de séance"

        def __str__(self):
            return self.title

class Multimedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    exercise = models.ManyToManyField(Personalisation.Exercice)
    theme = models.ManyToManyField(Personalisation.Theme)
    video = models.FileField(upload_to='videos_uploaded', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class SessionTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100)