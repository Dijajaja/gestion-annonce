# Guide de Déploiement

Ce guide vous explique comment déployer AdPlus sur différentes plateformes.

## 🚀 Déploiement sur Heroku

### Prérequis
- Compte Heroku
- Heroku CLI installé
- Git configuré

### Étapes

1. **Installation de Heroku CLI** (si pas déjà fait)
```bash
# Windows (avec Chocolatey)
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Connexion à Heroku**
```bash
heroku login
```

3. **Créer une application Heroku**
```bash
heroku create votre-app-name
```

4. **Configurer les variables d'environnement**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set ALLOWED_HOSTS=votre-app-name.herokuapp.com
```

5. **Configurer la base de données** (optionnel - PostgreSQL recommandé)
```bash
heroku addons:create heroku-postgresql:mini
```

6. **Déployer**
```bash
git push heroku main
```

7. **Exécuter les migrations**
```bash
heroku run python manage.py migrate
```

8. **Créer un superutilisateur**
```bash
heroku run python manage.py createsuperuser
```

9. **Collecter les fichiers statiques**
```bash
heroku run python manage.py collectstatic --noinput
```

Votre application sera disponible sur : `https://votre-app-name.herokuapp.com`

---

## 🌐 Déploiement sur Railway

1. **Créer un compte** sur [Railway](https://railway.app)

2. **Nouveau projet** : Cliquez sur "New Project" → "Deploy from GitHub repo"

3. **Sélectionner le dépôt** : `Dijajaja/gestion-annonce`

4. **Configurer les variables d'environnement** dans le dashboard :
   - `DEBUG=False`
   - `SECRET_KEY` (générez-en une nouvelle)
   - `ALLOWED_HOSTS=votre-domaine.up.railway.app`
   - Si vous utilisez PostgreSQL : `DATABASE_URL` sera automatiquement configuré

5. **Déployer** : Railway déploiera automatiquement à chaque push sur `main`

6. **Configurer le domaine** (optionnel) : Ajoutez votre domaine personnalisé dans les settings

---

## 📦 Déploiement sur Render

1. **Créer un compte** sur [Render](https://render.com)

2. **Nouveau Web Service** : Cliquez sur "New +" → "Web Service"

3. **Connecter le dépôt GitHub** : `Dijajaja/gestion-annonce`

4. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn plateforme_annonces.wsgi:application`
   - **Environment** : Python 3

5. **Variables d'environnement** :
   - `DEBUG=False`
   - `SECRET_KEY`
   - `ALLOWED_HOSTS=votre-service.onrender.com`
   - Si PostgreSQL : Créez une base de données PostgreSQL et utilisez `DATABASE_URL`

6. **Déploiement automatique** : Render déploiera à chaque push

---

## 🐳 Déploiement avec Docker (à venir)

Un Dockerfile sera ajouté prochainement pour faciliter le déploiement sur n'importe quelle plateforme supportant Docker.

---

## 📝 Variables d'environnement requises

### Obligatoires en production
```env
DEBUG=False
SECRET_KEY=votre_secret_key_aleatoire
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

### Optionnelles
```env
# Base de données MySQL
DATABASE_NAME=nom_db
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=https://votre-domaine.com

# SSL
SECURE_SSL_REDIRECT=True
```

---

## 🔒 Sécurité en Production

Assurez-vous de :

1. ✅ Mettre `DEBUG=False`
2. ✅ Utiliser une `SECRET_KEY` unique et sécurisée
3. ✅ Configurer `ALLOWED_HOSTS` correctement
4. ✅ Utiliser HTTPS (SSL)
5. ✅ Changer le mot de passe admin par défaut
6. ✅ Configurer une base de données sécurisée
7. ✅ Sauvegarder régulièrement la base de données

---

## 📊 Monitoring et Logs

### Heroku
```bash
heroku logs --tail
```

### Railway
Les logs sont visibles dans le dashboard

### Render
Les logs sont visibles dans le dashboard

---

## 🔄 Mises à jour

Pour mettre à jour votre application déployée :

1. Faire vos modifications localement
2. Committer et pousser :
```bash
git add .
git commit -m "Description des modifications"
git push origin main
```

3. Si déploiement automatique : Attendre le déploiement
4. Si manuel : Re-déployer selon votre plateforme

---

## ⚠️ Troubleshooting

### Erreur 500 en production
- Vérifiez les logs : `heroku logs --tail` (Heroku)
- Vérifiez que `DEBUG=False` est bien configuré
- Vérifiez que les migrations sont appliquées

### Fichiers statiques non chargés
- Exécutez : `python manage.py collectstatic --noinput`
- Vérifiez que WhiteNoise est dans `MIDDLEWARE`

### Base de données
- Vérifiez les variables d'environnement de la base de données
- Exécutez les migrations : `python manage.py migrate`

---

## 📞 Support

Pour toute question sur le déploiement, ouvrez une [issue](https://github.com/Dijajaja/gestion-annonce/issues) sur GitHub.

