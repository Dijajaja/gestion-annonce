from rest_framework import serializers
from .models import Annonce, Categorie

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['nom']

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = ['titre','description','prix','image','categorie','proprietaire','date_publication','status']

 # permettre de mettre à jour la catégorie via l'API, tu peux ajouter cette méthode
    def update(self, instance, validated_data):
        categorie_data = validated_data.pop('categorie')
        categorie = instance.categorie
        instance.titre = validated_data.get('titre', instance.titre)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Gérer la mise à jour de la catégorie
        instance.categorie.nom = categorie_data.get('nom', instance.categorie.nom)
        instance.categorie.save()
        return instance