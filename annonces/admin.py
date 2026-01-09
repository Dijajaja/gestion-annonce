from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Categorie, Annonce

# Enregistrez le modèle Categorie
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone', 'description', 'date_creation', 'annonce_count')
    list_filter = ('date_creation',)
    search_fields = ('nom', 'description')
    readonly_fields = ('date_creation',)
    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'icone')
        }),
        ('Dates', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    def annonce_count(self, obj):
        """Affiche le nombre d'annonces dans cette catégorie"""
        count = obj.annonce_set.count()
        return count
    annonce_count.short_description = _('Nombre d\'annonces')

# Enregistrez le modèle Annonce
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'titre', 'prix_display', 'categorie', 'proprietaire', 'status_badge', 'date_publication', 'vues')
    list_filter = ('categorie', 'status', 'date_publication', 'proprietaire')
    search_fields = ('titre', 'description', 'proprietaire__username', 'proprietaire__email')
    readonly_fields = ('date_publication', 'vues', 'image_preview')
    list_per_page = 25
    date_hierarchy = 'date_publication'
    
    fieldsets = (
        (_('Informations principales'), {
            'fields': ('titre', 'description', 'prix', 'categorie', 'proprietaire', 'status')
        }),
        (_('Image'), {
            'fields': ('image', 'image_preview')
        }),
        (_('Contact'), {
            'fields': ('telephone_contact', 'email_contact'),
            'classes': ('collapse',)
        }),
        (_('Localisation'), {
            'fields': ('ville', 'code_postal'),
            'classes': ('collapse',)
        }),
        (_('Statistiques'), {
            'fields': ('vues', 'date_publication'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['valider_annonces', 'rejeter_annonces', 'mettre_en_attente']
    
    def image_thumbnail(self, obj):
        """Affiche une miniature de l'image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<div style="width: 50px; height: 50px; background: #f0f0f0; border-radius: 4px; display: flex; align-items: center; justify-content: center;"><i class="fas fa-image" style="color: #999;"></i></div>')
    image_thumbnail.short_description = _('Image')
    
    def image_preview(self, obj):
        """Aperçu de l'image en grand"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px;" />',
                obj.image.url
            )
        return _('Aucune image')
    image_preview.short_description = _('Aperçu')
    
    def prix_display(self, obj):
        """Affiche le prix avec la devise MRU"""
        return obj.get_prix_display()
    prix_display.short_description = _('Prix')
    
    def status_badge(self, obj):
        """Affiche le statut avec un badge coloré"""
        colors = {
            'valide': 'green',
            'en_attente': 'orange',
            'rejet': 'red'
        }
        color = colors.get(obj.status, 'gray')
        status_text = {
            'valide': _('Validé'),
            'en_attente': _('En attente'),
            'rejet': _('Rejeté')
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            status_text.get(obj.status, obj.status)
        )
    status_badge.short_description = _('Statut')
    
    def valider_annonces(self, request, queryset):
        """Action pour valider plusieurs annonces"""
        updated = queryset.update(status='valide')
        self.message_user(request, _('{} annonce(s) validée(s) avec succès.').format(updated))
    valider_annonces.short_description = _('Valider les annonces sélectionnées')
    
    def rejeter_annonces(self, request, queryset):
        """Action pour rejeter plusieurs annonces"""
        updated = queryset.update(status='rejet')
        self.message_user(request, _('{} annonce(s) rejetée(s).').format(updated))
    rejeter_annonces.short_description = _('Rejeter les annonces sélectionnées')
    
    def mettre_en_attente(self, request, queryset):
        """Action pour remettre en attente plusieurs annonces"""
        updated = queryset.update(status='en_attente')
        self.message_user(request, _('{} annonce(s) mise(s) en attente.').format(updated))
    mettre_en_attente.short_description = _('Mettre en attente les annonces sélectionnées')