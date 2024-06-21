from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('settings/', views.settings, name='settings'),
    path('account/', views.account, name='account'),
    path('club/', views.club, name='club'),
    path('create-training/', views.create_training, name='create-training'),
]