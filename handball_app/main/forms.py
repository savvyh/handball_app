# forms.py
from django import forms
from .models import Profile, Category, Exercise, Multimedia, Theme

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
