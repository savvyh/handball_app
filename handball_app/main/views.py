# views.py
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .models import Favorite, Multimedia, Profile, Category, Theme, TrainingExercise, TrainingSession
from .forms import ProfileCreationForm, TrainingQuestionForm
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

def library(request):
    theme_filter = request.GET.get('theme', 'Tout')
    
    if theme_filter == 'Tout':
        multimedia = Multimedia.objects.all()
    else:
        multimedia = Multimedia.objects.filter(theme__name=theme_filter)
    
    themes = Theme.objects.all()
    return render(request, 'main/library.html', {
        'multimedia': multimedia,
        'themes': themes,
        'current_theme': theme_filter
    })

@login_required
def training(request):
    if request.method == 'POST':
        form = TrainingQuestionForm(request.POST)
        if form.is_valid():
            themes = form.cleaned_data['themes']
            category = form.cleaned_data['category']
            duration = form.cleaned_data['duration']
            intensity = form.cleaned_data['intensity']

            suggestions = get_suggestions(themes, category)

            return render(request, 'main/training_suggestions.html', {
                'suggestions': suggestions,
                'duration': duration,
                'intensity': intensity,
                'category': category
            })
    else:
        form = TrainingQuestionForm()
    return render(request, 'main/training.html', {'form': form})

def get_suggestions(themes, category):
    suggestions = Multimedia.objects.filter(theme__name__in=themes, categories=category)
    return suggestions

@login_required
def save_training_session(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        duration = request.POST.get('duration')
        intensity = request.POST.get('intensity')
        selected_videos = request.POST.getlist('videos')

        if not category_id:
            return render(request, 'main/error.html', {'message': 'Catégorie non spécifiée.'})

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return render(request, 'main/error.html', {'message': 'Catégorie non valide.'})

        training_session = TrainingSession.objects.create(
            title=title, 
            category=category, 
            duration=duration, 
            intensity=intensity, 
            user=request.user
        )

        for video_id in selected_videos:
            multimedia = Multimedia.objects.get(id=video_id)
            TrainingExercise.objects.create(training_session=training_session, multimedia=multimedia)

        return redirect('training_list')

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
            selected_categories = request.POST.getlist('categories')
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

@login_required
def add_favorite(request, multimedia_id):
    multimedia = get_object_or_404(Multimedia, id=multimedia_id)
    Favorite.objects.get_or_create(user=request.user, multimedia=multimedia)
    return redirect('library')

@login_required
def remove_favorite(request, multimedia_id):
    multimedia = get_object_or_404(Multimedia, id=multimedia_id)
    Favorite.objects.filter(user=request.user, multimedia=multimedia).delete()
    return redirect('library')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'main/favorite_list.html', {'favorites': favorites})

def admin_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_admin, login_url=login_url)

def member_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_member, login_url=login_url)
