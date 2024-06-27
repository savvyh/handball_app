from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur avec des messages d'erreur personnalisés.
    """
    username = forms.CharField(
        max_length=15,
        label="Nom d'utilisateur",
        error_messages={
            'max_length': "Nom d'utilisateur trop long (15 caractères maximum)",
            'required': "Ce champ est obligatoire."
        }
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': "Veuillez entrer une adresse e-mail valide.",
            'invalid': "Adresse e-mail invalide."
        }
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Veuillez entrer un mot de passe.",
        }
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Veuillez confirmer votre mot de passe.",
            'password_mismatch': "Les deux mots de passe ne correspondent pas.",
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    """
    Formulaire de connexion
    """
    username = forms.CharField(max_length=15, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

class UserUpdateForm(forms.ModelForm):
    """
    Formulaire pour la mise à jour des informations utilisateur.
    """
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': "Veuillez entrer une adresse e-mail valide.",
            'invalid': "Adresse e-mail invalide."
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'personal_informations', 'account_pref']
