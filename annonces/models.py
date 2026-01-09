from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from authentification.models import Utilisateur

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, blank=True, null=True, help_text="Nom de l'icône Font Awesome")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']

    def __str__(self):
        return self.nom
    
    def get_translated_nom(self):
        """Retourne le nom de la catégorie traduit"""
        from django.utils.translation import gettext as _
        # Utiliser gettext pour traduire le nom
        # Les traductions doivent être ajoutées dans les fichiers .po
        return _(self.nom)

class Annonce(models.Model):
    ETAT_CHOIX =[
        ('en_attente', _('En attente')),
        ('valide', _('Validé')),
        ('rejet', _('Rejeté')),
    ]
    TYPE_ANNONCE_CHOIX = [
        ('disponible', _('Disponible')),
        ('service', _('Service')),
        ('location', _('Location')),
        ('autre', _('Autre')),
    ]
    titre = models.CharField(max_length=255, verbose_name=_('Titre (Français)'))
    titre_en = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Titre (Anglais)'))
    description = models.TextField(verbose_name=_('Description (Français)'))
    description_en = models.TextField(blank=True, null=True, verbose_name=_('Description (Anglais)'))
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='images_annonces/', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ETAT_CHOIX, default='en_attente', max_length=20)
    statut_vente = models.CharField(choices=TYPE_ANNONCE_CHOIX, default='disponible', max_length=20, verbose_name=_('Type d\'annonce'))
    urgent = models.BooleanField(default=False, verbose_name=_('Urgent'))
    ville = models.CharField(max_length=100, blank=True, null=True, help_text="Ville où se trouve l'annonce")
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    telephone_contact = models.CharField(max_length=20, blank=True, null=True)
    email_contact = models.EmailField(blank=True, null=True)
    vues = models.IntegerField(default=0, help_text="Nombre de vues de l'annonce")
    favoris = models.ManyToManyField(Utilisateur, related_name='annonces_favorites', blank=True)

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['-date_publication']),
            models.Index(fields=['status']),
            models.Index(fields=['categorie']),
        ]

    def __str__(self):
        return self.titre
    
    def incrementer_vues(self):
        """Incrémente le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])
    
    def get_prix_display(self):
        """Retourne le prix formaté ou 'Gratuit'"""
        if self.prix:
            return f"{self.prix:.2f} MRU"
        return str(_("Gratuit"))
    
    def get_whatsapp_number(self):
        """Retourne le numéro de téléphone nettoyé pour WhatsApp"""
        if not self.telephone_contact:
            return None
        # Nettoyer le numéro : enlever espaces, tirets, parenthèses, et le + initial
        phone = str(self.telephone_contact).replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        return phone
    
    def get_translated_titre(self):
        """Retourne le titre traduit selon la langue active"""
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en' and self.titre_en:
            return self.titre_en
        return self.titre
    
    def get_translated_description(self):
        """Retourne la description traduite selon la langue active"""
        from django.utils import translation
        current_language = translation.get_language()
        if current_language == 'en' and self.description_en:
            return self.description_en
        return self.description
