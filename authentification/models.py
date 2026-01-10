from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Utilisateur(AbstractUser):
    ROLE_CHOIX =[
        ('admin','Admin'),
        ('client','Client'),
    ]
    telephone = models.CharField(max_length=20, blank=True, null=True, help_text="Format : +222 12 34 56 78")
    role = models.CharField(choices=ROLE_CHOIX, default='client', max_length=10)