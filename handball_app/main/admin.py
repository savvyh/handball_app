from django.contrib import admin
from .models import User, Category, TrainingSession, Multimedia, SessionTracking

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('session_title', 'category', 'session_date', 'user')
    search_fields = ('session_title', 'category', 'user__username')
    list_filter = ('session_date',)

@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('content_title', 'content_type', 'theme', 'user')
    search_fields = ('content_title', 'content_type', 'theme', 'user__username')
    list_filter = ('content_type', 'theme')

@admin.register(SessionTracking)
class SessionTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'training_session', 'theme')
    search_fields = ('user__username', 'training_session__session_title', 'theme')
