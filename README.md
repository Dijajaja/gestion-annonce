# AdPlus - Plateforme de Gestion d'Annonces

AdPlus est une plateforme web moderne et multilingue permettant aux utilisateurs de publier et gérer des annonces. Développée avec Django, elle offre une interface intuitive avec authentification, administration complète et support multilingue (Français/Anglais).

![Django](https://img.shields.io/badge/Django-5.1.6-092E20?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat&logo=bootstrap)

## ✨ Fonctionnalités

### Pour les Utilisateurs
- Authentification sécurisée : Inscription et connexion avec validation
- Gestion d'annonces : Créer, modifier et supprimer ses annonces
- Upload d'images : Ajouter des photos à vos annonces
- Recherche avancée : Filtrer par catégorie, prix, localisation
- Multilingue : Interface en Français et Anglais
- Responsive : Compatible mobile, tablette et desktop
- Thème sombre : Toggle entre mode clair et sombre

### Pour les Administrateurs
- 📊 Dashboard complet : Vue d'ensemble avec statistiques
- Validation d'annonces : Approuver ou rejeter les annonces
- Gestion des catégories: CRUD avec icônes Font Awesome
- Gestion des utilisateurs : Contrôle total sur les comptes
- Recherche et filtrage : Outils de recherche avancés

## 🚀 Installation Locale

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/Dijajaja/gestion-annonce.git
cd gestion-annonce
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```env
DEBUG=True
SECRET_KEY=votre_secret_key_ici
ALLOWED_HOSTS=localhost,127.0.0.1

# Optionnel : Configuration MySQL
# DATABASE_NAME=votre_db
# DATABASE_USER=votre_user
# DATABASE_PASSWORD=votre_password
# DATABASE_HOST=localhost
# DATABASE_PORT=3306
```

Pour générer une SECRET_KEY sécurisée :
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

5. *Appliquer les migrations*
```bash
python manage.py migrate
```

6. *Créer un superutilisateur*
```bash
python manage.py createsuperuser
```

7. *Collecter les fichiers statiques*
```bash
python manage.py collectstatic --noinput
```

8. *Lancer le serveur de développement*
```bash
python manage.py runserver
```

Accédez à l'application : http://127.0.0.1:8000/

## 📦 Déploiement

### Heroku

1. Installer Heroku CLI
2. Créer un compte Heroku
3. Déployer :
```bash
heroku create votre-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=votre_secret_key
heroku config:set ALLOWED_HOSTS=votre-app-name.herokuapp.com
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Railway / Render

Ces plateformes détectent automatiquement Django. Configurez simplement les variables d'environnement dans le dashboard :
- `DEBUG=False`
- `SECRET_KEY` (générez-en une nouvelle)
- `ALLOWED_HOSTS=votre-domaine.com`
- Optionnellement les variables MySQL si vous utilisez une base de données externe



## 📁 Structure du Projet

```
gestion-annonce/
├── authentification/     # App d'authentification
├── annonces/            # App principale des annonces
├── plateforme_annonces/ # Configuration Django
├── templates/           # Templates de base
├── static/              # Fichiers statiques
├── media/               # Images uploadées
├── locale/              # Traductions (FR/EN)
├── screenshots/         # Captures d'écran
├── PRODUCTION.md        # Guide de production
├── TRANSLATION.md       # Guide de traduction
└── requirements.txt     # Dépendances Python
```

## 🌐 Internationalisation

L'application supporte le Français (par défaut) et l'Anglais. 

Pour ajouter une nouvelle langue :
1. `python manage.py makemessages -l [code_langue]`
2. Éditer les fichiers `.po` dans `locale/[code_langue]/LC_MESSAGES/`
3. `python manage.py compilemessages`

Voir [TRANSLATION.md](TRANSLATION.md) pour plus de détails.

## 🔒 Sécurité

En production, les paramètres suivants sont automatiquement activés :
- ✅ SSL/HTTPS redirection
- ✅ Cookies sécurisés
- ✅ Protection XSS
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Protection CSRF

Voir [PRODUCTION.md](PRODUCTION.md) pour la configuration complète.


## 🛠️ Technologies Utilisées

- **Backend** : Django 5.1.6
- **Frontend** : Bootstrap 5, Font Awesome 6
- **Base de données** : SQLite (développement) / MySQL (production)
- **API** : Django REST Framework avec JWT
- **Images** : Pillow
- **i18n** : Django i18n


## 📄 Licence

Ce projet est sous licence MIT.

## 👥 Auteur

Développé avec ❤️ pour la gestion d'annonces.

## 📞 Support

Pour toute question ou problème, ouvrez une [issue](https://github.com/Dijajaja/gestion-annonce/issues) sur GitHub.

---

**⭐ N'oubliez pas de mettre une étoile si ce projet vous a été utile !**
