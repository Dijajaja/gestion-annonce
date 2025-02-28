# annonces/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Annonce, Categorie
from .forms import AnnonceAdminForm, CategorieForm
from authentification.models import Utilisateur
from django.views.decorators.csrf import csrf_exempt


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('liste_annonces')
    
    annonces = Annonce.objects.all()
    categories = Categorie.objects.all()
    return render(request, 'dashboard/admin_dashboard.html', {'annonces': annonces, 'categories': categories})

@csrf_exempt
def valider_annonce(request, annonce_id):
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': "Vous n'avez pas les permissions nécessaires."}, status=403)
    
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        action = request.POST.get('action')  # 'valider' ou 'rejeter'
        if action == 'valider':
            annonce.status = 'valide'
        elif action == 'rejeter':
            annonce.status = 'rejet'
        else:
            return JsonResponse({'success': False, 'error': "Action non reconnue."}, status=400)
        
        annonce.save()
        return JsonResponse({'success': True, 'status': annonce.status, 'message': f"L'annonce a été {action}ée avec succès."})
    return JsonResponse({'success': False, 'error': "Méthode non autorisée."}, status=405)

# Les autres vues restent inchangées (modifier, supprimer, créer annonces et catégories)

@login_required
def modifier_annonce_admin(request, annonce_id):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        form = AnnonceAdminForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            form.save()
            messages.success(request, "L'annonce a été modifiée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = AnnonceAdminForm(instance=annonce)
    return render(request, 'dashboard/modifier_annonce_admin.html', {'form': form, 'annonce': annonce})

@login_required
def supprimer_annonce_admin(request, annonce_id):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        annonce.delete()
        messages.success(request, "L'annonce a été supprimée avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'dashboard/supprimer_annonce_admin.html', {'annonce': annonce})

@login_required
def creer_annonce_admin(request):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AnnonceAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "L'annonce a été créée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = AnnonceAdminForm()
    return render(request, 'dashboard/creer_annonce_admin.html', {'form': form})

@login_required
def liste_categories(request):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    categories = Categorie.objects.all()
    return render(request, 'dashboard/liste_categories.html', {'categories': categories})

@login_required
def creer_categorie(request):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La catégorie a été créée avec succès.")
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'dashboard/creer_categorie.html', {'form': form})

@login_required
def modifier_categorie(request, categorie_id):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, "La catégorie a été modifiée avec succès.")
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'dashboard/modifier_categorie.html', {'form': form, 'categorie': categorie})

@login_required
def supprimer_categorie(request, categorie_id):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, "La catégorie a été supprimée avec succès.")
        return redirect('liste_categories')
    return render(request, 'dashboard/supprimer_categorie.html', {'categorie': categorie})