from django.db import models
from django.contrib.auth.models import User
from authentification.models import Utilisateur

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Annonce(models.Model):
    ETAT_CHOIX =[
        ('en_attente','En attente'),
        ('valide','Validé'),
        ('rejet', 'Rejeté'),
    ]
    titre = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='images_annonces/', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    proprietaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ETAT_CHOIX, default='en_attente', max_length=20)

    def __str__(self):
        return self.titre
