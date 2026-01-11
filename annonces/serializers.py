from rest_framework import serializers
from .models import Annonce, Categorie
from authentification.models import Utilisateur


class UtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs (lecture seule dans les annonces)"""
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email']


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description', 'icone', 'date_creation']


class AnnonceSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(),
        source='categorie',
        write_only=True,
        required=False,
        allow_null=True
    )
    proprietaire = UtilisateurSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Annonce
        fields = [
            'id', 'titre', 'titre_en', 'description', 'description_en',
            'prix', 'image', 'image_url', 'categorie', 'categorie_id',
            'proprietaire', 'date_publication', 'date_modification',
            'status', 'statut_vente', 'urgent', 'ville', 'code_postal',
            'telephone_contact', 'email_contact', 'vues'
        ]
        read_only_fields = ['proprietaire', 'date_publication', 'date_modification', 'vues']

    def get_image_url(self, obj):
        """Retourne l'URL complète de l'image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None