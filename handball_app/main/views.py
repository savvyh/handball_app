import datetime, locale
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .models import Favorite, Multimedia, Profile, Category, Theme, TrainingExercise, TrainingSession
from .forms import ProfileCreationForm, TrainingQuestionForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django import template
from django.utils import timezone


register = template.Library()

def landing(request):
    return render(request, 'main/landing.html')

@login_required
def home(request):
    profiles = Profile.objects.filter(user=request.user)
    latest_videos = Multimedia.objects.order_by('-created_at')[:3]
    for video in latest_videos:
        print(video.categories.all())
    return render(request, 'main/home.html', {'profiles': profiles, 'latest_videos': latest_videos})

def subscribe(request):
    return render(request, 'main/subscribe.html')

@login_required
def personal_space(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id, user=request.user)
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist")
    
    today = timezone.now().date()
    past_sessions = TrainingSession.objects.filter(user=request.user, date__lt=today)
    upcoming_sessions = TrainingSession.objects.filter(user=request.user, date__gte=today)
    
    return render(request, 'main/personal_space.html', {
        'profile': profile,
        'past_sessions': past_sessions,
        'upcoming_sessions': upcoming_sessions
    })

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

def get_suggestions(themes, category):
    suggestions = Multimedia.objects.filter(theme__name__in=themes, categories=category)
    return suggestions

@login_required
def training(request):
    if request.method == 'POST':
        form = TrainingQuestionForm(request.POST)
        if form.is_valid():
            themes = form.cleaned_data['themes']
            category = form.cleaned_data['category']
            duration = form.cleaned_data['duration']
            intensity = form.cleaned_data['intensity']
            date = form.cleaned_data['date']

            suggestions = get_suggestions(themes, category)

            return render(request, 'main/training_intermediate.html', {
                'suggestions': suggestions,
                'duration': duration,
                'intensity': intensity,
                'category': category,
                'date': date  # Pass the date here
            })
    else:
        form = TrainingQuestionForm()
    return render(request, 'main/training.html', {'form': form})

@login_required
def training_intermediate(request):
    if request.method == 'POST':
        selected_exercises = request.POST.getlist('exercises')
        category = request.POST.get('category')
        duration = request.POST.get('duration')
        intensity = request.POST.get('intensity')
        date = request.POST.get('date')
        
        return render(request, 'main/training_finalize.html', {
            'selected_exercises': selected_exercises,
            'category': category,
            'duration': duration,
            'intensity': intensity,
            'date': date  
        })

@login_required
def training_finalize(request):
    if request.method == 'POST':
        selected_exercises = request.POST.getlist('exercises')
        category = request.POST.get('category')
        duration = request.POST.get('duration')
        intensity = request.POST.get('intensity')
        date = request.POST.get('date')
        theme = request.POST.get('theme')
        remaining_time = int(duration[:-1]) * 60  # Calcul du temps restant en minutes

        # Calculer le temps total des vidéos sélectionnées
        total_video_time = 0
        for video_id in selected_exercises:
            video = Multimedia.objects.get(id=video_id)
            h, m, s = map(int, video.video_time.split(':'))
            video_duration = h * 3600 + m * 60 + s
            total_video_time += video_duration

        remaining_time -= total_video_time // 60  # Mise à jour du temps restant

        # Créer ou récupérer une session d'entraînement et l'ajouter à la session
        training_session = TrainingSession.objects.create(
            title="Séance personnalisée",
            category=Category.objects.get(id=category),
            duration=duration,
            intensity=intensity,
            user=request.user,
            date=date
        )
        request.session['training_session_id'] = training_session.id

        return render(request, 'main/training_finalize.html', {
            'selected_exercises': selected_exercises,
            'category': category,
            'duration': duration,
            'intensity': intensity,
            'date': date,
            'theme': theme,
            'remaining_time': remaining_time
        })

    all_videos = Multimedia.objects.all()
    selected_exercises = request.session.get('selected_exercises', [])
    return render(request, 'main/training_finalize.html', {
        'selected_exercises': selected_exercises,
        'all_videos': all_videos
    })

@login_required
def save_training_session(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        duration = request.POST.get('duration')
        intensity = request.POST.get('intensity')
        date_str = request.POST.get('date')  # Récupérer la date de la séance
        selected_videos = request.POST.getlist('videos')

        if not category_id:
            return render(request, 'main/error.html', {'message': 'Catégorie non spécifiée.'})

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return render(request, 'main/error.html', {'message': 'Catégorie non valide.'})

        try:

            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            date_obj = datetime.datetime.strptime(date_str, "%d %B %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return render(request, 'main/error.html', {'message': 'Format de date invalide.'})

        profile, created = Profile.objects.get_or_create(user=request.user, defaults={'name': request.user.username})

        training_session = TrainingSession.objects.create(
            title=title, 
            category=category, 
            duration=duration, 
            intensity=intensity, 
            user=request.user,
            date=formatted_date
        )

        for video_id in selected_videos:
            multimedia = Multimedia.objects.get(id=video_id)
            TrainingExercise.objects.create(training_session=training_session, multimedia=multimedia)

        return redirect('personal_space', profile_id=profile.id)
    
      
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

def video_detail(request, video_id):
    video = get_object_or_404(Multimedia, id=video_id)
    return redirect('library')

@login_required
def remove_video(request, video_id):
    if request.method == 'POST':
        training_session_id = request.session.get('training_session_id')
        if not training_session_id:
            return redirect('training_finalize')
        training_session = get_object_or_404(TrainingSession, id=training_session_id)
        video_id = request.POST.get('video_id')
        try:
            training_exercise = TrainingExercise.objects.get(training_session=training_session, multimedia_id=video_id)
            training_exercise.delete()
        except TrainingExercise.DoesNotExist:
            pass
        return redirect('training_finalize')

@login_required
def add_video(request):
    if request.method == 'POST':
        video_id = request.POST.get('video')
        if not video_id:
            return redirect('library')
        training_session_id = request.session.get('training_session_id')
        if not training_session_id:
            return redirect('training')
        training_session = get_object_or_404(TrainingSession, id=training_session_id)
        video = get_object_or_404(Multimedia, id=video_id)
        TrainingExercise.objects.create(training_session=training_session, multimedia=video)
        return redirect('library')