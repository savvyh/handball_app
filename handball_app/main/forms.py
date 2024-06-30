from django import forms
from .models import Profile, Category

class ProfileCreationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Catégories"
    )

    class Meta:
        model = Profile
        fields = ['name', 'categories', 'profile_image']
