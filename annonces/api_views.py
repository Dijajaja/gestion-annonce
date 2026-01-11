"""
Vues API REST pour l'application annonces
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Annonce, Categorie
from .serializers import AnnonceSerializer, CategorieSerializer
from authentification.models import Utilisateur


class CategorieViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les catégories
    - Liste : GET /api/categories/
    - Détail : GET /api/categories/{id}/
    - Créer : POST /api/categories/ (admin seulement)
    - Modifier : PUT/PATCH /api/categories/{id}/ (admin seulement)
    - Supprimer : DELETE /api/categories/{id}/ (admin seulement)
    """
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'date_creation']
    ordering = ['nom']

    def get_permissions(self):
        """
        Les actions de modification nécessitent l'authentification admin
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Vérifier que l'utilisateur est admin avant de créer"""
        if not (self.request.user.is_staff or self.request.user.role == 'admin'):
            raise PermissionDenied("Seuls les administrateurs peuvent créer des catégories")
        serializer.save()
    
    def perform_update(self, serializer):
        """Vérifier que l'utilisateur est admin avant de modifier"""
        if not (self.request.user.is_staff or self.request.user.role == 'admin'):
            raise PermissionDenied("Seuls les administrateurs peuvent modifier des catégories")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier que l'utilisateur est admin avant de supprimer"""
        if not (self.request.user.is_staff or self.request.user.role == 'admin'):
            raise PermissionDenied("Seuls les administrateurs peuvent supprimer des catégories")
        instance.delete()


class AnnonceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les annonces
    """
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'ville']
    ordering_fields = ['date_publication', 'prix', 'vues']
    ordering = ['-date_publication']

    def get_queryset(self):
        """
        Retourne les annonces selon le contexte :
        - Public : seulement les annonces validées
        - Authentifié (client) : ses propres annonces
        - Admin : toutes les annonces
        """
        user = self.request.user
        
        if not user.is_authenticated:
            # Public : seulement validées
            return Annonce.objects.filter(status='valide')
        
        if user.role == 'admin' or user.is_staff:
            # Admin : toutes les annonces
            queryset = Annonce.objects.all()
        else:
            # Client : ses annonces ou les validées
            queryset = Annonce.objects.filter(
                Q(proprietaire=user) | Q(status='valide')
            )
        
        # Filtres optionnels
        status_filter = self.request.query_params.get('status', None)
        if status_filter and (user.role == 'admin' or user.is_staff):
            queryset = queryset.filter(status=status_filter)
        
        categorie_id = self.request.query_params.get('categorie', None)
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        
        prix_min = self.request.query_params.get('prix_min', None)
        if prix_min:
            try:
                queryset = queryset.filter(prix__gte=float(prix_min))
            except ValueError:
                pass
        
        prix_max = self.request.query_params.get('prix_max', None)
        if prix_max:
            try:
                queryset = queryset.filter(prix__lte=float(prix_max))
            except ValueError:
                pass
        
        ville = self.request.query_params.get('ville', None)
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        
        return queryset

    def get_permissions(self):
        """
        Permissions selon l'action
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Créer une annonce pour l'utilisateur connecté"""
        serializer.save(proprietaire=self.request.user)

    def perform_update(self, serializer):
        """Vérifier que l'utilisateur peut modifier cette annonce"""
        annonce = self.get_object()
        user = self.request.user
        
        # Admin peut tout modifier, sinon seulement ses propres annonces
        if not (user.role == 'admin' or user.is_staff) and annonce.proprietaire != user:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres annonces")
        
        serializer.save()

    def perform_destroy(self, instance):
        """Vérifier que l'utilisateur peut supprimer cette annonce"""
        user = self.request.user
        if not (user.role == 'admin' or user.is_staff) and instance.proprietaire != user:
            raise PermissionDenied("Vous ne pouvez supprimer que vos propres annonces")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def valider(self, request, pk=None):
        """Action pour valider une annonce (admin seulement)"""
        annonce = self.get_object()
        if not (request.user.role == 'admin' or request.user.is_staff):
            return Response(
                {'error': 'Seuls les administrateurs peuvent valider des annonces'},
                status=status.HTTP_403_FORBIDDEN
            )
        annonce.status = 'valide'
        annonce.save()
        serializer = self.get_serializer(annonce)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rejeter(self, request, pk=None):
        """Action pour rejeter une annonce (admin seulement)"""
        annonce = self.get_object()
        if not (request.user.role == 'admin' or request.user.is_staff):
            return Response(
                {'error': 'Seuls les administrateurs peuvent rejeter des annonces'},
                status=status.HTTP_403_FORBIDDEN
            )
        annonce.status = 'rejet'
        annonce.save()
        serializer = self.get_serializer(annonce)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def incrementer_vues(self, request, pk=None):
        """Incrémenter le compteur de vues"""
        annonce = self.get_object()
        annonce.incrementer_vues()
        serializer = self.get_serializer(annonce)
        return Response(serializer.data)

