from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.signup, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('authentification/', views.authentification, name='authentification'),
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="register/password_reset.html"), 
         name="password_reset"),
    path('reset_password_done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="register/password_reset_done.html"), 
         name="password_reset_done"),
    path('reset_password_confirm/<uidb64>/<token>/', 
         views.CustomPasswordResetConfirmView.as_view(template_name="register/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="register/password_reset_complete.html"), 
         name="password_reset_complete"),
]
