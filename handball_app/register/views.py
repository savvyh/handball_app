from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
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