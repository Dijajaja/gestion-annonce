# annonces/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Annonce, Categorie
from authentification.models import *

class TranslatedFileInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['data-button-text'] = str(_('Choisir un fichier'))
        self.attrs['data-no-file-text'] = str(_('Aucun fichier choisi'))

class AnnonceCreationForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'titre_en', 'description', 'description_en', 'prix', 'image', 'categorie', 'statut_vente', 'ville', 'code_postal', 'telephone_contact', 'email_contact', 'urgent']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Titre de l\'annonce (Français)')}),
            'titre_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Titre de l\'annonce (Anglais) - Optionnel')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Description détaillée de l\'annonce (Français)')}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Description détaillée de l\'annonce (Anglais) - Optionnel')}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'image': TranslatedFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'statut_vente': forms.Select(attrs={'class': 'form-select'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ville')}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Code postal')}),
            'telephone_contact': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('exemple@email.com')}),
            'urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titre': _('Titre (Français)'),
            'titre_en': _('Titre (Anglais) - Optionnel'),
            'description': _('Description (Français)'),
            'description_en': _('Description (Anglais) - Optionnel'),
            'prix': _('Prix (MRU)'),
            'image': _('Image'),
            'categorie': _('Catégorie'),
            'statut_vente': _('Type d\'annonce'),
            'ville': _('Ville'),
            'code_postal': _('Code postal'),
            'telephone_contact': _('Téléphone de contact'),
            'email_contact': _('Email de contact'),
            'urgent': _('Urgent'),
        }

class AnnonceAdminForm(forms.ModelForm):
    proprietaire = forms.ModelChoiceField(
        queryset=Utilisateur.objects.all(),
        label=_("Propriétaire"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_publication = forms.DateTimeField(
        label=_('Date de publication'),
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        help_text=_("La date sera automatiquement définie si laissée vide")
    )

    class Meta:
        model = Annonce
        fields = ['titre', 'titre_en', 'description', 'description_en', 'prix', 'image', 'categorie', 'proprietaire', 'status', 'statut_vente', 'urgent', 'telephone_contact', 'email_contact']
        
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Titre de l\'annonce (Français)')}),
            'titre_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Titre de l\'annonce (Anglais) - Optionnel')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Description détaillée de l\'annonce (Français)')}),
            'description_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Description détaillée de l\'annonce (Anglais) - Optionnel')}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'image': TranslatedFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'statut_vente': forms.Select(attrs={'class': 'form-select'}),
            'urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telephone_contact': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('exemple@email.com')}),
        }
        labels = {
            'titre': _('Titre (Français)'),
            'titre_en': _('Titre (Anglais) - Optionnel'),
            'description': _('Description (Français)'),
            'description_en': _('Description (Anglais) - Optionnel'),
            'prix': _('Prix (MRU)'),
            'image': _('Image'),
            'categorie': _('Catégorie'),
            'status': _('Statut'),
            'statut_vente': _('Type d\'annonce'),
            'urgent': _('Urgent'),
            'telephone_contact': _('Téléphone de contact'),
            'email_contact': _('Email de contact'),
        }

class CategorieForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Exemple: Immobilier, Automobile, Électronique...'),
            'required': True,
            'id': 'id_categorie_nom'
        }),
        label=_("Nom de la catégorie"),
        help_text=_('Nom de la catégorie qui sera affiché dans l\'application.'),
        max_length=100,
        required=True
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': _('Description de la catégorie (optionnel)'),
            'id': 'id_categorie_description'
        }),
        label=_("Description"),
        help_text=_('Description optionnelle de la catégorie pour aider les utilisateurs.'),
        required=False
    )
    
    icone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('fa-home, fa-car, fa-laptop...'),
            'id': 'id_categorie_icone',
            'pattern': '^fa-[a-z0-9-]+$'
        }),
        label=_("Icône Font Awesome"),
        help_text=_('Nom de l\'icône Font Awesome (ex: fa-home, fa-car). L\'icône sera affichée à droite.'),
        max_length=50,
        required=False
    )
    
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'icone']
    
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if nom:
            nom = nom.strip()
            if len(nom) < 2:
                raise forms.ValidationError(_('Le nom de la catégorie doit contenir au moins 2 caractères.'))
            if len(nom) > 100:
                raise forms.ValidationError(_('Le nom de la catégorie ne peut pas dépasser 100 caractères.'))
        return nom
    
    def clean_icone(self):
        icone = self.cleaned_data.get('icone')
        if icone:
            icone = icone.strip()
            # Enlever les préfixes fa- ou fas fa- si présents
            if icone.startswith('fa-'):
                pass  # Bon format
            elif icone.startswith('fas fa-'):
                icone = icone.replace('fas fa-', 'fa-')
            elif icone.startswith('far fa-'):
                icone = icone.replace('far fa-', 'fa-')
            elif icone.startswith('fab fa-'):
                icone = icone.replace('fab fa-', 'fa-')
            elif not icone.startswith('fa-'):
                icone = f'fa-{icone}'
        return icone