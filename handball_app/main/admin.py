from django.contrib import admin
from .models import User, Category, TrainingSession, Multimedia, SessionTracking, Personalisation

admin.site.register(User)
admin.site.register(Category)
admin.site.register(TrainingSession)
admin.site.register(Multimedia)
admin.site.register(SessionTracking)
admin.site.register(Personalisation.Exercice)
admin.site.register(Personalisation.Theme)
