from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Profile, Category
from .forms import ProfileCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

def landing(request):
    return render(request, 'main/landing.html')

@login_required
def home(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'main/home.html', {'profiles': profiles})

def subscribe(request):
    return render(request, 'main/subscribe.html')

@login_required
def personal_space(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id, user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'main/personal_space.html', {'profile': profile})

def club(request):
    return render(request, 'main/club.html')

def settings(request):
    return render(request, 'main/settings.html')

def create_training(request):
    return render(request, 'main/create-training.html')

def training(request):
    return render(request, 'main/training.html')

@login_required
def create_profile(request):
    if not request.user.can_add_profile():
        return redirect('home')
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            selected_categories = request.POST.get('categories').split(',')
            profile.categories.set(selected_categories)
            profile.save()
            request.user.profile_completed = True
            request.user.save()
            return redirect('home')
    else:
        form = ProfileCreationForm(user=request.user)
    categories = Category.objects.all()
    return render(request, 'main/create_profile.html', {'form': form, 'categories': categories})


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileCreationForm
    template_name = 'main/create_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        selected_categories = self.request.POST.getlist('categories')
        self.object.categories.set(selected_categories)
        self.object.save()
        self.request.user.profile_completed = True
        self.request.user.save()
        return response

class ProfileListView(ListView):
    model = Profile
    template_name = 'main/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
