# forms.py
from django import forms
from .models import Profile, Category, Exercise, Multimedia, Theme, TrainingSession

class ProfileCreationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Catégories"
    )

    class Meta:
        model = Profile
        fields = ['name', 'categories', 'profile_image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileCreationForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Profile.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("Ce nom de profil est déjà utilisé. Veuillez en choisir un autre.")
        return name

class MultimediaCreationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Catégories"
    )
    theme = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Thèmes"
    )

    class Meta:
        model = Multimedia
        fields = ['title', 'description', 'exercise', 'theme', 'categories', 'video', 'video_time', 'other_file', 'creator']

    def __init__(self, *args, **kwargs):
        super(MultimediaCreationForm, self).__init__(*args, **kwargs)


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['title', 'category', 'duration', 'intensity']

class TrainingQuestionForm(forms.Form):
    theme_choices = [
        ('Attaque', 'Attaque'),
        ('Défense', 'Défense'),
        ('Techniques', 'Techniques'),
        ('Spécifique', 'Spécifique'),
        ('Cohésion', 'Cohésion'),
        ('Physique', 'Physique')
    ]
    themes = forms.MultipleChoiceField(choices=theme_choices, widget=forms.CheckboxSelectMultiple, label="Qu'aimeriez-vous travailler aujourd'hui ? (Max 3 choix)")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Pour quelle catégorie ?")
    duration = forms.ChoiceField(choices=[('1h', '1h'), ('1h30', '1h30'), ('2h', '2h')], label="Durée de l'entraînement")
    intensity = forms.ChoiceField(choices=[('faible', 'Faible'), ('moyenne', 'Moyenne'), ('élevée', 'Élevée')], label="Intensité de l'entraînement")
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date de la séance")