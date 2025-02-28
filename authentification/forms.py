# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur

class InscriptionForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'telephone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-input'}),
            'telephone': forms.NumberInput(attrs={'class': 'form-control custom-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control custom-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control custom-input'}),
        }
        
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nom d'utilisateur"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Mot de passe"
    )