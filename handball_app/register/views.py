from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()  
    return render(request, 'register/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'register/connexion.html', {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    else:
        form = CustomLoginForm()
    return render(request, 'register/connexion.html', {'form': form})


def authentification(request):
    form_login = CustomLoginForm()
    form_register = CustomUserCreationForm()
    return render(request, 'register/authentification.html', {'form_login': form_login, 'form_register': form_register})


def deconnexion(request):
    logout(request)
    return redirect('index')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('login'))