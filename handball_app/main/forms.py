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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileCreationForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Profile.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("Ce nom de profil est déjà utilisé. Veuillez en choisir un autre.")
        return name