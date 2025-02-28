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
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from authentification.models import *
from django.http import JsonResponse
# annonces/views.py (ajoutez après la vue liste_annonces)

@login_required
def modifier_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, proprietaire=request.user)  # Vérifie que l'utilisateur est le propriétaire
    if request.method == 'POST':
        form = AnnonceCreationForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            return redirect('liste_annonces')  # Redirige vers la liste après modification
    else:
        form = AnnonceCreationForm(instance=annonce)
    return render(request, 'modifier_annonce.html', {'form': form, 'annonce': annonce})

@login_required
def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, proprietaire=request.user)  # Vérifie que l'utilisateur est le propriétaire
    if request.method == 'POST':
        annonce.delete()
        return redirect('liste_annonces')  # Redirige vers la liste des annonces après suppression
    return redirect('liste_annonces')

@login_required
def creer_annonce(request):
    if request.method == 'POST':
        form = AnnonceCreationForm(request.POST, request.FILES)  # Inclut request.FILES pour gérer l'image
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.proprietaire = request.user  # Associe l'annonce à l'utilisateur connecté
            annonce.status = 'en_attente'  # Définit le statut par défaut
            annonce.save()
            return redirect('liste_annonces')  # Redirige vers la liste des annonces après création
    else:
        form = AnnonceCreationForm()
    
    return render(request, 'creer_annonce.html', {'form': form})

def liste_annonces(request):
    status = request.GET.get('status', None)
    if request.user.is_authenticated :
        if request.user.role == 'admin' :
            return redirect('admin_dashboard')
        else:
            if status:
                annonces = Annonce.objects.filter(proprietaire=request.user, status=status)
            else:
                annonces = Annonce.objects.filter(proprietaire=request.user)
            return render(request, 'liste_annonces.html', {'annonces': annonces, 'status': status})
    else:
        annonces = Annonce.objects.all()
    return render(request, 'home.html', {'annonces': annonces})

def detail_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)  # Récupère l'annonce ou renvoie une 404 si non trouvée
    return render(request, 'detail_annonce.html', {'annonce': annonce})


@api_view(['GET','POST'])
def liste_annonces_api(request):
    if request.method == 'GET':
        annonce = Annonce.objects.all()
        serializer = AnnonceSerializer(annonce, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = AnnonceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def detail_annonce_api(request, pk):
    
    try:
        annonce = Annonce.objects.get(pk=pk)
    except Annonce.DoesNotExist:
        return  Response({"error": "Annonce non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AnnonceSerializer(annonce)
        return Response(serializer.data)

    elif  request.method == 'PUT':
        serializer = AnnonceSerializer(annonce, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        annonce.delete()
        return Response({"message": "Annonces supprimé avec succès"}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def liste_annonces_api(request, serializer=None):
    if request.method == 'GET':
        annonce = Annonce.objects.all().order_by('date_publication')
        serializer = AnnonceSerializer(annonce, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


