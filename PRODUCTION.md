# Guide de Configuration pour la Production

## Configuration des Variables d'Environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Configuration Django
DEBUG=False
SECRET_KEY=votre_secret_key_tres_long_et_aleatoire_ici
ALLOWED_HOSTS=localhost,127.0.0.1,votre-domaine.com

# Configuration Base de données MySQL (optionnel)
# Si ces variables ne sont pas définies, SQLite sera utilisé par défaut
DATABASE_NAME=votre_nom_db
DATABASE_USER=votre_utilisateur
DATABASE_PASSWORD=votre_mot_de_passe
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Configuration CORS (optionnel)
CORS_ALLOWED_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com

# Configuration SSL (optionnel, pour HTTPS)
SECURE_SSL_REDIRECT=True
```

## Génération d'une SECRET_KEY sécurisée

Pour générer une SECRET_KEY sécurisée, utilisez :

```python
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

## Collecte des fichiers statiques

Avant de déployer en production, collectez les fichiers statiques :

```bash
python manage.py collectstatic --noinput
```

## Identifiants Admin

**Identifiants par défaut :**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT : Changez ce mot de passe immédiatement en production !**

Pour changer le mot de passe :
```bash
python manage.py changepassword admin
```

## Déploiement

1. Configurez les variables d'environnement dans votre fichier `.env`
2. Assurez-vous que `DEBUG=False` en production
3. Configurez `ALLOWED_HOSTS` avec votre domaine
4. Collectez les fichiers statiques : `python manage.py collectstatic`
5. Configurez votre serveur web (Nginx, Apache) pour servir les fichiers statiques
6. Utilisez un serveur WSGI comme Gunicorn ou uWSGI

## Sécurité

Les paramètres de sécurité suivants sont automatiquement activés lorsque `DEBUG=False` :
- SSL/HTTPS redirection
- Cookies sécurisés
- Protection XSS
- HSTS (HTTP Strict Transport Security)

