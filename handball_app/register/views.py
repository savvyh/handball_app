from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_admin = True
            user.profile_limit = 10
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register/login.html', {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    else:
        form = CustomLoginForm()
    return render(request, 'register/login.html', {'form': form})

def authentification(request):
    form_login = CustomLoginForm()
    form_register = CustomUserCreationForm()
    return render(request, 'register/authentification.html', {'form_login': form_login, 'form_register': form_register})

def logout_view(request):
    logout(request)
    return redirect('landing')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('login'))

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'register/user_profile.html', {'form': form})
