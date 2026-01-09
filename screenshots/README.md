# Captures d'écran de l'application

Ce dossier contient toutes les captures d'écran des pages de l'application AdPlus.

## Pages capturées

### Pages publiques (5)
1. **portfolio_full.png** - Page Portfolio (Accueil)
2. **liste_annonces_full.png** - Liste des annonces publiques
3. **connexion_full.png** - Page de connexion
4. **inscription_full.png** - Page d'inscription
5. **detail_annonce_full.png** - Détail d'une annonce

### Pages admin (6)
1. **admin_dashboard_full.png** - Tableau de bord admin
2. **admin_categories_full.png** - Liste des catégories (admin)
3. **admin_creer_annonce_full.png** - Créer une annonce (admin)
4. **admin_creer_categorie_full.png** - Créer une catégorie (admin)
5. **admin_modifier_annonce_full.png** - Modifier une annonce (admin)
6. **admin_modifier_categorie_full.png** - Modifier une catégorie (admin)

## Comment recapturer

Pour recapturer toutes les pages, exécutez :

```bash
python capture_all_pages.py
```

**Note:** Assurez-vous que le serveur Django est en cours d'exécution (`python manage.py runserver`) et que vous êtes connecté en tant qu'admin pour les pages admin.

## Scripts disponibles

- `capture_all_pages.py` - Script principal pour capturer toutes les pages automatiquement
- `capture_screenshots.py` - Script pour générer la liste des URLs à capturer

