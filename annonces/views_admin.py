# annonces/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Annonce, Categorie
from .forms import AnnonceAdminForm, CategorieForm
from authentification.models import Utilisateur
from django.contrib.auth.models import Group

def est_dans_groupe(user, groupes):
    return user.groups.filter(name__in=groupes).exists()

def est_admin(user):
    """Vérifie si l'utilisateur est admin (par rôle ou superuser)"""
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def admin_dashboard(request):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    # Statistiques
    total_annonces = Annonce.objects.count()
    annonces_validees = Annonce.objects.filter(status='valide').count()
    annonces_en_attente = Annonce.objects.filter(status='en_attente').count()
    annonces_rejetees = Annonce.objects.filter(status='rejet').count()
    total_categories = Categorie.objects.count()
    total_utilisateurs = Utilisateur.objects.count()
    total_clients = Utilisateur.objects.filter(role='client').count()
    total_admins = Utilisateur.objects.filter(role='admin').count()
    
    # Calcul du taux de validation
    taux_validation = 0.0
    if total_annonces > 0:
        taux_validation = round((annonces_validees * 100.0) / total_annonces, 1)
    
    # Statistiques par catégorie
    from django.db.models import Count
    stats_par_categorie = Annonce.objects.values('categorie__nom').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Statistiques par type d'annonce
    stats_par_type = Annonce.objects.values('statut_vente').annotate(
        count=Count('id')
    )
    
    # Statistiques par mois (7 derniers mois)
    from django.utils import timezone
    from datetime import timedelta
    import json
    
    stats_par_mois = []
    mois_labels = []
    for i in range(6, -1, -1):
        date_debut = timezone.now() - timedelta(days=30*i)
        date_fin = timezone.now() - timedelta(days=30*(i-1)) if i > 0 else timezone.now()
        count = Annonce.objects.filter(
            date_publication__gte=date_debut,
            date_publication__lt=date_fin
        ).count()
        mois_nom = date_debut.strftime('%b %Y')
        stats_par_mois.append(count)
        mois_labels.append(mois_nom)
    
    # Préparer les données pour les graphiques
    categories_labels = [item['categorie__nom'] or 'Sans catégorie' for item in stats_par_categorie]
    categories_data = [item['count'] for item in stats_par_categorie]
    
    type_labels = []
    type_data = []
    type_colors = {
        'disponible': '#10b981',
        'service': '#3b82f6',
        'location': '#f59e0b',
        'autre': '#6b7280'
    }
    for item in stats_par_type:
        type_labels.append(item['statut_vente'] or 'Autre')
        type_data.append(item['count'])
    
    # Filtres
    status_filter = request.GET.get('status', '')
    categorie_filter = request.GET.get('categorie', '')
    search_query = request.GET.get('q', '')
    
    annonces = Annonce.objects.all()
    
    if status_filter:
        annonces = annonces.filter(status=status_filter)
    if categorie_filter:
        annonces = annonces.filter(categorie_id=categorie_filter)
    if search_query:
        annonces = annonces.filter(
            Q(titre__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(proprietaire__username__icontains=search_query)
        )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(annonces.order_by('-date_publication'), 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    categories = Categorie.objects.all()
    
    context = {
        'annonces': page_obj,
        'categories': categories,
        'total_annonces': total_annonces,
        'annonces_validees': annonces_validees,
        'annonces_en_attente': annonces_en_attente,
        'annonces_rejetees': annonces_rejetees,
        'total_categories': total_categories,
        'total_utilisateurs': total_utilisateurs,
        'total_clients': total_clients,
        'total_admins': total_admins,
        'taux_validation': taux_validation,
        'status_filter': status_filter,
        'categorie_filter': categorie_filter,
        'search_query': search_query,
        # Données pour les graphiques
        'categories_labels': json.dumps(categories_labels),
        'categories_data': json.dumps(categories_data),
        'type_labels': json.dumps(type_labels),
        'type_data': json.dumps(type_data),
        'mois_labels': json.dumps(mois_labels),
        'mois_data': json.dumps(stats_par_mois),
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def valider_annonce(request, annonce_id):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        action = request.POST.get('action') 
        if action == 'valider':
            annonce.status = 'valide'
        elif action == 'rejeter':
            annonce.status = 'rejet'
        annonce.save()
    return redirect('admin_dashboard')


@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def modifier_annonce_admin(request, annonce_id):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        form = AnnonceAdminForm(request.POST, request.FILES, instance=annonce)
        if form.is_valid():
            # Sauvegarder avec commit=False pour gérer date_publication manuellement
            annonce = form.save(commit=False)
            # Gérer date_publication manuellement
            date_pub = form.cleaned_data.get('date_publication')
            if date_pub:
                annonce.date_publication = date_pub
            # Sauvegarder l'instance existante (pas de création)
            annonce.save()
            # Si on a défini manuellement la date, s'assurer qu'elle est bien sauvegardée
            if date_pub:
                Annonce.objects.filter(pk=annonce.pk).update(date_publication=date_pub)
            messages.success(request, "L'annonce a été modifiée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = AnnonceAdminForm(instance=annonce)
    return render(request, 'dashboard/modifier_annonce_admin.html', {'form': form, 'annonce': annonce})

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def supprimer_annonce_admin(request, annonce_id):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        annonce.delete()
        messages.success(request, "L'annonce a été supprimée avec succès.")
        return redirect('admin_dashboard')
    return render(request, 'dashboard/supprimer_annonce_admin.html', {'annonce': annonce})

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def creer_annonce_admin(request):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AnnonceAdminForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            # Gérer date_publication manuellement car auto_now_add empêche la modification
            date_pub = form.cleaned_data.get('date_publication')
            if date_pub:
                # Utiliser la date fournie
                annonce.date_publication = date_pub
            # Sinon, laisser auto_now_add définir la date automatiquement
            annonce.save()
            # Si on a défini manuellement la date, il faut la sauvegarder à nouveau
            # car auto_now_add peut l'écraser
            if date_pub:
                Annonce.objects.filter(pk=annonce.pk).update(date_publication=date_pub)
            messages.success(request, "L'annonce a été créée avec succès.")
            return redirect('admin_dashboard')
    else:
        form = AnnonceAdminForm()
    return render(request, 'dashboard/creer_annonce_admin.html', {'form': form})

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def liste_categories(request):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    categories = Categorie.objects.all()
    return render(request, 'dashboard/liste_categories.html', {'categories': categories})

@login_required
@user_passes_test(est_admin, login_url='/connexion/')
def creer_categorie(request):
    if not est_admin(request.user):
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
@user_passes_test(est_admin, login_url='/connexion/')
def modifier_categorie(request, categorie_id):
    if not est_admin(request.user):
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
@user_passes_test(est_admin, login_url='/connexion/')
def supprimer_categorie(request, categorie_id):
    if not est_admin(request.user):
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('admin_dashboard')
    
    categorie = get_object_or_404(Categorie, id=categorie_id)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, "La catégorie a été supprimée avec succès.")
        return redirect('liste_categories')
    return render(request, 'dashboard/supprimer_categorie.html', {'categorie': categorie})