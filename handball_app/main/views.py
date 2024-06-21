from django.shortcuts import render

def landing(request):
    return render(request, 'main/landing.html')

def home(request):
    return render(request, 'main/home.html')

def subscribe(request):
    return render(request, 'main/subscribe.html')

def account(request):
    return render(request, 'main/account.html')

def club(request):
    return render(request, 'main/club.html')

def settings(request):
    return render(request, 'main/settings.html')

def create_training(request):
    return render(request, 'main/create-training.html')
