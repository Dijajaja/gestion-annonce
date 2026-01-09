# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import InscriptionForm, ConnexionForm
from django.contrib.auth.models import Group

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            groupe, created = Group.objects.get_or_create(name='client')
            utilisateur.groups.add(groupe)
            return redirect('connexion') 
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
                # Rediriger les admins (par rôle ou superuser) vers le dashboard admin
                if request.user.role == 'admin' or request.user.is_superuser:
                    return redirect('admin_dashboard') 
                else:
                    return redirect('liste_annonces_user')
            
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect('portfolio')