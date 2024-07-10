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
    path('training/', views.training, name='training'),
    path('training_intermediate/', views.training_intermediate, name='training_intermediate'),
    path('training_finalize/', views.training_finalize, name='training_finalize'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('library/', views.library, name='library'),
    path('add_favorite/<int:multimedia_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:multimedia_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('save_training_session/', views.save_training_session, name='save_training_session'),
]