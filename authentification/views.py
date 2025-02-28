# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, 'Inscription réussie!')
            return redirect('liste_annonces')  # Remplacez par votre vue d'accueil
    else:
        form = InscriptionForm()
    
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            utilisateur = authenticate(username=username, password=password)
            if utilisateur is not None:
                login(request, utilisateur)
                messages.success(request, 'Vous êtes connecté!')
                if request.user.role == 'admin':
                    return redirect('admin_dashboard')  # Remplacez par votre vue d'accueil
                else:
                    return redirect('liste_annonces')
            else:
                messages.error(request, 'Identifiants invalides')
    else:
        form = ConnexionForm()
    
    return render(request, 'connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect('liste_annonces')