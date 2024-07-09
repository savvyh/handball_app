from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, TrainingSession, Multimedia, SessionTracking, Theme, Exercise
from .forms import MultimediaCreationForm

class MultimediaAdmin(admin.ModelAdmin):
    form = MultimediaCreationForm
    list_display = ['title', 'exercise', 'video_time']
    search_fields = ['title', 'exercise']

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'is_member', 'is_guest')}),
    )
    list_filter = BaseUserAdmin.list_filter + ('is_admin', 'is_member', 'is_guest')

admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(TrainingSession)
admin.site.register(SessionTracking)
admin.site.register(Theme)
admin.site.register(Exercise)
admin.site.register(Multimedia, MultimediaAdmin)