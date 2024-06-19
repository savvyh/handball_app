from django.shortcuts import render

def landing(request):
    return render(request, 'main/landing.html')

def home(request):
    return render(request, 'main/home.html')
