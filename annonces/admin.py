from django.contrib import admin
from .models import Categorie, Annonce  # Importez vos modèles

# Enregistrez le modèle Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)  # Affiche le champ 'nom' dans la liste des catégories
    search_fields = ('nom',)  # Permet de rechercher par nom

# Enregistrez le modèle Annonce
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'prix', 'categorie', 'proprietaire', 'date_publication', 'status')
    list_filter = ('categorie', 'proprietaire', 'date_publication', 'status')  # Filtres dans la sidebar
    search_fields = ('titre', 'description')  # Permet de rechercher par titre ou description
    readonly_fields = ('date_publication',)  # Empêche la modification de la date de publication

    # Optionnel : Personnaliser l'affichage des champs dans le formulaire d'administration
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'prix', 'image', 'categorie', 'proprietaire', 'status')
        }),
        ('Dates', {
            'fields': ('date_publication',),
            'classes': ('collapse',)  # Masque cette section par défaut
        }),
    )