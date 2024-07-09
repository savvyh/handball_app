from django.contrib import admin
from .models import User, Category, TrainingSession, Multimedia, SessionTracking, Theme, Exercise
from .forms import MultimediaCreationForm

class MultimediaAdmin(admin.ModelAdmin):
    form = MultimediaCreationForm
    list_display = ['title', 'exercise', 'theme', 'video_time']
    search_fields = ['title', 'exercise']


admin.site.register(User)
admin.site.register(Category)
admin.site.register(TrainingSession)
admin.site.register(SessionTracking)
admin.site.register(Theme)
admin.site.register(Exercise)
admin.site.register(Multimedia, MultimediaAdmin)
