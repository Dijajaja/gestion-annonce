from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur(AbstractUser):
    ROLE_CHOIX =[
        ('admin','Admin'),
        ('client','Client'),
    ]
    telephone = models.IntegerField(blank=True,null=True)
    role = models.CharField(choices=ROLE_CHOIX, default='client', max_length=10)