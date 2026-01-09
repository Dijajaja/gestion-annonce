"""
Script pour capturer automatiquement des captures d'écran de toutes les pages de l'application
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plateforme_annonces.settings')
django.setup()

from django.test import Client
from annonces.models import Annonce, Categorie
from authentification.models import Utilisateur
import json

def get_test_urls():
    """Génère la liste de toutes les URLs à capturer"""
    base_url = "http://127.0.0.1:8000"
    urls = []
    
    # Récupérer des IDs d'exemple pour les URLs avec paramètres
    first_annonce = Annonce.objects.first()
    first_categorie = Categorie.objects.first()
    first_user = Utilisateur.objects.first()
    
    # Pages publiques
    urls.append({
        'name': 'portfolio',
        'url': f'{base_url}/',
        'description': 'Page Portfolio (Accueil)'
    })
    
    urls.append({
        'name': 'liste_annonces',
        'url': f'{base_url}/app/',
        'description': 'Liste des annonces publiques'
    })
    
    if first_annonce:
        urls.append({
            'name': 'detail_annonce',
            'url': f'{base_url}/annonces/{first_annonce.id}/',
            'description': f'Détail de l\'annonce: {first_annonce.titre}'
        })
    
    # Pages d'authentification
    urls.append({
        'name': 'connexion',
        'url': f'{base_url}/connexion/',
        'description': 'Page de connexion'
    })
    
    urls.append({
        'name': 'inscription',
        'url': f'{base_url}/inscription/',
        'description': 'Page d\'inscription'
    })
    
    # Pages admin (nécessitent authentification - à capturer après connexion)
    urls.append({
        'name': 'admin_dashboard',
        'url': f'{base_url}/admins/',
        'description': 'Tableau de bord admin',
        'requires_auth': True
    })
    
    urls.append({
        'name': 'admin_categories',
        'url': f'{base_url}/admins/categories/',
        'description': 'Liste des catégories (admin)',
        'requires_auth': True
    })
    
    urls.append({
        'name': 'admin_creer_annonce',
        'url': f'{base_url}/admins/creer/',
        'description': 'Créer une annonce (admin)',
        'requires_auth': True
    })
    
    if first_annonce:
        urls.append({
            'name': 'admin_modifier_annonce',
            'url': f'{base_url}/admins/modifier/{first_annonce.id}/',
            'description': f'Modifier annonce {first_annonce.id} (admin)',
            'requires_auth': True
        })
    
    if first_categorie:
        urls.append({
            'name': 'admin_modifier_categorie',
            'url': f'{base_url}/admins/categories/modifier/{first_categorie.id}/',
            'description': f'Modifier catégorie {first_categorie.id} (admin)',
            'requires_auth': True
        })
    
    urls.append({
        'name': 'admin_creer_categorie',
        'url': f'{base_url}/admins/categories/creer/',
        'description': 'Créer une catégorie (admin)',
        'requires_auth': True
    })
    
    # Pages utilisateur connecté
    urls.append({
        'name': 'mes_annonces',
        'url': f'{base_url}/mes-annonces/',
        'description': 'Mes annonces (utilisateur)',
        'requires_auth': True,
        'role': 'client'
    })
    
    urls.append({
        'name': 'creer_annonce',
        'url': f'{base_url}/creer/',
        'description': 'Créer une annonce (utilisateur)',
        'requires_auth': True,
        'role': 'client'
    })
    
    if first_annonce:
        urls.append({
            'name': 'modifier_annonce',
            'url': f'{base_url}/modifier/{first_annonce.id}/',
            'description': f'Modifier annonce {first_annonce.id} (utilisateur)',
            'requires_auth': True,
            'role': 'client'
        })
    
    return urls

def create_urls_list():
    """Crée un fichier JSON avec toutes les URLs à capturer"""
    urls = get_test_urls()
    output = {
        'base_url': 'http://127.0.0.1:8000',
        'pages': urls,
        'instructions': {
            'public': 'Ces pages peuvent être capturées sans authentification',
            'requires_auth': 'Ces pages nécessitent une connexion (admin ou client)',
            'note': 'Pour les pages nécessitant authentification, connectez-vous d\'abord manuellement'
        }
    }
    
    # Créer le dossier screenshots s'il n'existe pas
    os.makedirs('screenshots', exist_ok=True)
    
    # Sauvegarder la liste
    with open('screenshots/urls_list.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # Créer un fichier texte lisible
    with open('screenshots/urls_list.txt', 'w', encoding='utf-8') as f:
        f.write("=== LISTE DES PAGES À CAPTURER ===\n\n")
        f.write("BASE URL: http://127.0.0.1:8000\n\n")
        
        f.write("PAGES PUBLIQUES:\n")
        f.write("-" * 50 + "\n")
        for url_info in [u for u in urls if not u.get('requires_auth')]:
            f.write(f"{url_info['description']}\n")
            f.write(f"URL: {url_info['url']}\n")
            f.write(f"Nom: {url_info['name']}\n\n")
        
        f.write("\nPAGES ADMIN (necessitent connexion admin):\n")
        f.write("-" * 50 + "\n")
        for url_info in [u for u in urls if u.get('requires_auth') and not u.get('role')]:
            f.write(f"{url_info['description']}\n")
            f.write(f"URL: {url_info['url']}\n")
            f.write(f"Nom: {url_info['name']}\n\n")
        
        f.write("\nPAGES UTILISATEUR (necessitent connexion client):\n")
        f.write("-" * 50 + "\n")
        for url_info in [u for u in urls if u.get('role') == 'client']:
            f.write(f"{url_info['description']}\n")
            f.write(f"URL: {url_info['url']}\n")
            f.write(f"Nom: {url_info['name']}\n\n")
    
    print(f"Liste creee avec {len(urls)} pages")
    print(f"Fichiers crees:")
    print(f"   - screenshots/urls_list.json")
    print(f"   - screenshots/urls_list.txt")
    print(f"\nPour capturer automatiquement, installez playwright:")
    print(f"   pip install playwright")
    print(f"   playwright install chromium")
    
    return urls

if __name__ == '__main__':
    create_urls_list()

