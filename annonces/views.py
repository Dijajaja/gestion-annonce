from http.client import responses
from django.core.serializers import serialize
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils.representation import serializer_repr
from .models import Annonce, Categorie
from .serializers import AnnonceSerializer, CategorieSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *
from authentification.models import *
from django.contrib.auth.models import Group

def est_dans_groupe(user, groupes):
    print(user.groups)
    return user.groups.filter(name__in=groupes).exists()

@login_required
@user_passes_test(lambda u: est_dans_groupe(u, ['client']), login_url='/connexion/')
def modifier_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, proprietaire=request.user)  
    if request.method == 'POST':
        form = AnnonceCreationForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, 'Votre annonce a été modifiée avec succès.')
            return redirect('liste_annonces_user')  
    else:
        form = AnnonceCreationForm(instance=annonce)
    return render(request, 'modifier_annonce.html', {'form': form, 'annonce': annonce})

@login_required
@user_passes_test(lambda u: est_dans_groupe(u, ['client']), login_url='/connexion/')
def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, proprietaire=request.user) 
    if request.method == 'POST':
        annonce.delete()
        from django.contrib import messages
        messages.success(request, 'Votre annonce a été supprimée avec succès.')
        return redirect('liste_annonces_user') 
    return redirect('liste_annonces_user')

@login_required
@user_passes_test(lambda u: est_dans_groupe(u, ['client']), login_url='/connexion/')
def creer_annonce(request):
    if request.method == 'POST':
        form = AnnonceCreationForm(request.POST, request.FILES) 
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.proprietaire = request.user 
            annonce.status = 'en_attente' 
            annonce.save()
            from django.contrib import messages
            messages.success(request, 'Votre annonce a été créée avec succès et est en attente de validation.')
            return redirect('liste_annonces_user')  
    else:
        form = AnnonceCreationForm()
    
    return render(request, 'creer_annonce.html', {'form': form})

@login_required
@user_passes_test(lambda u: est_dans_groupe(u, ['client']), login_url='/connexion/')
def liste_annonces_user(request):
    if request.user.is_authenticated :
        if request.user.role == 'admin' :
            return redirect('admin_dashboard')
        else:
            annonces = Annonce.objects.filter(proprietaire=request.user)  # type: ignore
            
            # Filtrage par statut
            status_filter = request.GET.get('status', '')
            if status_filter:
                annonces = annonces.filter(status=status_filter)
            
            return render(request, 'liste_annonces.html', {'annonces': annonces, 'status': status_filter})
    else:
        annonces = Annonce.objects.filter(status='valide')  # type: ignore
    return render(request, 'home.html', {'annonces': annonces})

def portfolio_page(request):
    """Page portfolio - Page d'accueil principale"""
    return render(request, 'portfolio.html')

def liste_annonces(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from django.db.models import Q
    
    # Si l'utilisateur est admin, rediriger vers le dashboard
    if request.user.is_authenticated and request.user.role == 'admin':
        return redirect('admin_dashboard')
    
    # Récupération des paramètres de recherche et filtrage
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie', '')
    prix_min = request.GET.get('prix_min', '')
    prix_max = request.GET.get('prix_max', '')
    ville = request.GET.get('ville', '')
    tri = request.GET.get('tri', 'date_desc')  # date_desc, date_asc, prix_asc, prix_desc
    
    # Afficher toutes les annonces validées pour tous les utilisateurs (Explorer)
    annonces = Annonce.objects.filter(status='valide')  # type: ignore
    
    # Filtrage par recherche
    if query:
        annonces = annonces.filter(
            Q(titre__icontains=query) |  # type: ignore
            Q(description__icontains=query) |  # type: ignore
            Q(ville__icontains=query)
        )
    
    # Filtrage par catégorie
    if categorie_id:
        annonces = annonces.filter(categorie_id=categorie_id)
    
    # Filtrage par prix
    if prix_min:
        try:
            annonces = annonces.filter(prix__gte=float(prix_min))
        except ValueError:
            pass
    if prix_max:
        try:
            annonces = annonces.filter(prix__lte=float(prix_max))
        except ValueError:
            pass
    
    # Filtrage par ville
    if ville:
        annonces = annonces.filter(ville__icontains=ville)
    
    # Tri
    if tri == 'date_asc':
        annonces = annonces.order_by('date_publication')
    elif tri == 'prix_asc':
        annonces = annonces.order_by('prix')
    elif tri == 'prix_desc':
        annonces = annonces.order_by('-prix')
    else:  # date_desc par défaut
        annonces = annonces.order_by('-date_publication')
    
    # Pagination
    paginator = Paginator(annonces, 12)  # 12 annonces par page
    page = request.GET.get('page', 1)
    try:
        annonces_page = paginator.page(page)
    except PageNotAnInteger:
        annonces_page = paginator.page(1)
    except EmptyPage:
        annonces_page = paginator.page(paginator.num_pages)
    
    # Récupération des catégories pour le filtre
    categories = Categorie.objects.all()  # type: ignore
    
    context = {
        'annonces': annonces_page,
        'categories': categories,
        'query': query,
        'categorie_id': categorie_id,
        'prix_min': prix_min,
        'prix_max': prix_max,
        'ville': ville,
        'tri': tri,
    }
    
    # Ajouter le nombre total d'annonces pour les stats
    if hasattr(annonces_page, 'paginator'):
        context['total_annonces'] = annonces_page.paginator.count
    
    return render(request, 'home.html', context)

def detail_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    
    # Incrémenter le compteur de vues si l'annonce est validée
    if annonce.status == 'valide':
        annonce.incrementer_vues()
    
    # Récupérer des annonces similaires (même catégorie)
    annonces_similaires = Annonce.objects.filter(  # type: ignore
        categorie=annonce.categorie,
        status='valide'
    ).exclude(id=annonce.id)[:4]
    
    return render(request, 'detail_annonce.html', {
        'annonce': annonce,
        'annonces_similaires': annonces_similaires
    })


# @api_view(['GET','POST'])
# def liste_annonces_api(request):
#     if request.method == 'GET':
#         annonce = Annonce.objects.all()
#         serializer = AnnonceSerializer(annonce, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = AnnonceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def detail_annonce_api(request, pk):
    
#     try:
#         annonce = Annonce.objects.get(pk=pk)
#     except Annonce.DoesNotExist:
#         return  Response({"error": "Annonce non trouvé"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = AnnonceSerializer(annonce)
#         return Response(serializer.data)

#     elif  request.method == 'PUT':
#         serializer = AnnonceSerializer(annonce, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         annonce.delete()
#         return Response({"message": "Annonces supprimé avec succès"}, status=status.HTTP_200_OK)

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def liste_annonces_api(request, serializer=None):
#     if request.method == 'GET':
#         annonce = Annonce.objects.all().order_by('date_publication')
#         serializer = AnnonceSerializer(annonce, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


