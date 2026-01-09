# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import Utilisateur

class InscriptionForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Entrez votre nom d\'utilisateur'),
            'autocomplete': 'username',
            'required': True
        }),
        label=_("Nom d'utilisateur"),
        help_text=_('150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.'),
        max_length=150,
        required=True
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('exemple@email.com'),
            'autocomplete': 'email',
            'required': True
        }),
        label=_("Adresse électronique"),
        required=True
    )
    
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('+222 12 34 56 78'),
            'autocomplete': 'tel',
            'pattern': '[0-9+\\s\\-\\(\\)]+'
        }),
        label=_("Téléphone"),
        required=False,
        help_text=_('Format : +222 12 34 56 78 (optionnel)')
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Minimum 8 caractères'),
            'autocomplete': 'new-password',
            'id': 'id_password1',
            'required': True
        }),
        label=_("Mot de passe"),
        help_text=_('Votre mot de passe doit contenir au moins 8 caractères.'),
        required=True
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirmez votre mot de passe'),
            'autocomplete': 'new-password',
            'id': 'id_password2',
            'required': True
        }),
        label=_("Confirmation du mot de passe"),
        help_text=_('Entrez le même mot de passe qu\'avant, pour vérification.'),
        required=True
    )
    
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ['username', 'email', 'telephone', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 3:
            raise forms.ValidationError(_('Le nom d\'utilisateur doit contenir au moins 3 caractères.'))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Un compte avec cet email existe déjà.'))
        return email
        
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Entrez votre nom d\'utilisateur'),
            'autocomplete': 'username',
            'id': 'id_username_login',
            'required': True,
            'autofocus': True
        }),
        label=_("Nom d'utilisateur"),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Entrez votre mot de passe'),
            'autocomplete': 'current-password',
            'id': 'id_password_login',
            'required': True
        }),
        label=_("Mot de passe"),
        required=True
    )
    
    error_messages = {
        'invalid_login': _(
            "Veuillez entrer un nom d'utilisateur et un mot de passe valides. "
            "Notez que les champs peuvent être sensibles à la casse."
        ),
        'inactive': _("Ce compte est inactif."),
    }