# annonces/forms.py
from django import forms
from .models import Annonce, Categorie
from authentification.models import *

class AnnonceCreationForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-input', 'rows': 4}),
            'prix': forms.NumberInput(attrs={'class': 'form-control custom-input', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control custom-input'}),
            'categorie': forms.Select(attrs={'class': 'form-control custom-input'}),
        }

class AnnonceAdminForm(forms.ModelForm):
    proprietaire = forms.ModelChoiceField(
        queryset=Utilisateur.objects.all(),
        label="Propriétaire",
        widget=forms.Select(attrs={'class': 'form-control custom-input'})
    )

    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie', 'proprietaire', 'status']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control custom-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-input', 'rows': 4}),
            'prix': forms.NumberInput(attrs={'class': 'form-control custom-input', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control custom-input'}),
            'categorie': forms.Select(attrs={'class': 'form-control custom-input'}),
            'status': forms.Select(attrs={'class': 'form-control custom-input'}),
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control custom-input'}),
        }