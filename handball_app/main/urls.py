from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', include('register.urls')),
    path('home/', views.home, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('settings/', views.settings, name='settings'),
    path('personal_space/<int:profile_id>/', views.personal_space, name='personal_space'),
    path('club/', views.club, name='club'),
    path('create-training/', views.create_training, name='create-training'),
    path('create-profile/', views.create_profile, name='create_profile'),
]
