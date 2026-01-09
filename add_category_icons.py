"""
Script pour ajouter des icônes Font Awesome à toutes les catégories
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plateforme_annonces.settings')
django.setup()

from annonces.models import Categorie

# Mapping des catégories avec leurs icônes appropriées
CATEGORY_ICONS = {
    'Immobilier': 'fas fa-home',
    'Mode': 'fas fa-tshirt',
    'Véhicules': 'fas fa-car',
    'Électronique': 'fas fa-laptop',
    'Formation': 'fas fa-graduation-cap',
    'Maison & Jardin': 'fas fa-home',
    'Sport & Loisirs': 'fas fa-futbol',
    'Services': 'fas fa-tools',
    'Emploi': 'fas fa-briefcase',
    'Animaux': 'fas fa-paw',
    'Multimédia': 'fas fa-tv',
    'Informatique': 'fas fa-desktop',
    'Téléphonie': 'fas fa-mobile-alt',
    'Meubles': 'fas fa-couch',
    'Décoration': 'fas fa-palette',
    'Jardinage': 'fas fa-seedling',
    'Bricolage': 'fas fa-hammer',
    'Vêtements': 'fas fa-tshirt',
    'Chaussures': 'fas fa-shoe-prints',
    'Accessoires': 'fas fa-gem',
    'Beauté': 'fas fa-spa',
    'Santé': 'fas fa-heartbeat',
    'Livres': 'fas fa-book',
    'Musique': 'fas fa-music',
    'Jeux': 'fas fa-gamepad',
    'Jouets': 'fas fa-puzzle-piece',
    'Bébé': 'fas fa-baby',
    'Autre': 'fas fa-tag',
}

def update_category_icons():
    """Met à jour les icônes de toutes les catégories"""
    categories = Categorie.objects.all()
    updated = 0
    created = 0
    
    print("Mise à jour des icônes des catégories...\n")
    
    for category in categories:
        nom = category.nom
        if nom in CATEGORY_ICONS:
            if not category.icone or category.icone != CATEGORY_ICONS[nom]:
                category.icone = CATEGORY_ICONS[nom]
                category.save()
                print(f"OK {nom}: {CATEGORY_ICONS[nom]}")
                updated += 1
            else:
                print(f"- {nom}: deja configuree ({category.icone})")
        else:
            print(f"! {nom}: aucune icone definie (categorie non mappee)")
    
    # Créer les catégories manquantes avec leurs icônes
    print("\nVérification des catégories manquantes...\n")
    for nom, icone in CATEGORY_ICONS.items():
        if not Categorie.objects.filter(nom=nom).exists():
            Categorie.objects.create(nom=nom, icone=icone)
            print(f"+ {nom}: créée avec icône {icone}")
            created += 1
    
    print(f"\nOK {updated} categorie(s) mise(s) a jour")
    print(f"OK {created} categorie(s) creee(s)")
    print("\nToutes les icônes ont été configurées !")

if __name__ == '__main__':
    update_category_icons()

