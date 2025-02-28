# authentification/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    # Définir les champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'role', 'telephone', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')  # Filtres dans la barre latérale
    search_fields = ('username', 'email', 'role')  # Champ de recherche
    ordering = ('-date_joined',)  # Tri par défaut par date de création décroissante
    
    # Définir les champs pour le formulaire d’ajout et d’édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Définir les champs requis lors de la création d’un nouvel utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telephone', 'role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    # Rendre certains champs non modifiables (par exemple, les dates automatiques)
    readonly_fields = ('last_login', 'date_joined')

# Enregistrer le modèle Utilisateur avec la classe Admin personnalisée
admin.site.register(Utilisateur, UtilisateurAdmin)