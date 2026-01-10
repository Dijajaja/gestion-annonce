# 🚀 Guide de Déploiement sur Render

Ce guide détaillé vous explique comment déployer AdPlus sur Render étape par étape.

## 📋 Prérequis

- ✅ Compte GitHub (votre code est déjà sur GitHub)
- ✅ Compte Render (gratuit disponible sur [render.com](https://render.com))
- ✅ Votre dépôt GitHub : `https://github.com/Dijajaja/gestion-annonce`

## 🎯 Étapes de Déploiement

### Étape 1 : Créer un compte Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur **"Get Started"** ou **"Sign Up"**
3. Choisissez **"Sign up with GitHub"** pour connecter votre compte GitHub

### Étape 2 : Créer un nouveau Web Service

1. Dans le dashboard Render, cliquez sur **"New +"** en haut à droite
2. Sélectionnez **"Web Service"**
3. Connectez votre dépôt GitHub si ce n'est pas déjà fait
4. Sélectionnez le dépôt : **`Dijajaja/gestion-annonce`**

### Étape 3 : Configurer le Service

Remplissez les champs suivants :

**Informations de base :**
- **Name** : `adplus` (ou le nom de votre choix)
- **Region** : Choisissez la région la plus proche (ex: `Oregon (US West)`)
- **Branch** : `main`
- **Root Directory** : *(laissez vide - le projet est à la racine)*

**Build & Deploy :**
- **Environment** : `Python 3`
- **Build Command** :
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command** :
  ```bash
  gunicorn plateforme_annonces.wsgi:application
  ```

### Étape 4 : Configurer les Variables d'Environnement

Dans la section **"Environment Variables"**, ajoutez les variables suivantes :

#### Variables Obligatoires :

1. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: *(générez une clé sécurisée)*
   
   Pour générer une SECRET_KEY :
   ```bash
   python manage.py shell
   >>> from django.core.management.utils import get_random_secret_key
   >>> print(get_random_secret_key())
   ```
   Copiez la clé générée et collez-la comme valeur.

3. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `votre-service.onrender.com` *(sera automatiquement fourni après le déploiement)*
   
   ⚠️ **Important** : Après le premier déploiement, Render vous donnera une URL comme `adplus-xxxx.onrender.com`. Mettez à jour cette variable avec cette URL complète.

#### Variables Optionnelles (si vous utilisez une base de données externe) :

Si vous souhaitez utiliser PostgreSQL sur Render :

1. **Créer une base de données PostgreSQL** :
   - Dans le dashboard Render, cliquez sur **"New +"** → **"PostgreSQL"**
   - Choisissez un nom et un plan (gratuit disponible)
   - Une fois créée, notez la **Internal Database URL** et **External Database URL**

2. **Configurer les variables de base de données** :
   - Key: `DATABASE_URL`
   - Value: *(l'URL fournie par Render)*
   
   Render fournit automatiquement `DATABASE_URL` si vous créez une base PostgreSQL dans le même projet.

### Étape 5 : Déployer

1. Cliquez sur **"Create Web Service"** en bas de la page
2. Render va commencer à construire et déployer votre application
3. Cela peut prendre 5-10 minutes la première fois
4. Surveillez les logs pour voir la progression

### Étape 6 : Configurer la Base de Données

⚠️ **IMPORTANT : Limitation du plan gratuit Render**
- Le plan gratuit permet **une seule base de données PostgreSQL gratuite**
- Si vous avez déjà une base, réutilisez-la ou supprimez l'ancienne
- Vous pouvez aussi utiliser SQLite pour les tests (mais données perdues lors des redéploiements)

#### Option A : Utiliser PostgreSQL sur Render (Recommandé)

1. **Créer la base PostgreSQL** (si pas déjà fait ET si vous n'avez pas d'autre base gratuite) :
   - **New +** → **PostgreSQL**
   - Plan gratuit disponible : `Free`
   - ⚠️ **Si erreur "cannot have more than one active free tier database"** :
     - Vous avez déjà une base PostgreSQL gratuite
     - Soit supprimez l'ancienne (Settings → Delete Database)
     - Soit réutilisez l'existante (voir ci-dessous)

2. **Lier la base à votre service** :
   - **Si vous créez une nouvelle base** : Render la détectera automatiquement et ajoutera `DATABASE_URL`
   - **Si vous réutilisez une base existante** :
     1. Allez dans votre base PostgreSQL existante sur Render
     2. Copiez l'**"Internal Database URL"** ou **"External Database URL"**
     3. Dans votre Web Service → **Environment Variables**
     4. Ajoutez : Key = `DATABASE_URL`, Value = l'URL copiée
     5. Cliquez sur "Save Changes"

3. **Modifier settings.py pour utiliser DATABASE_URL** :

   Vous devrez peut-être modifier `plateforme_annonces/settings.py` pour utiliser `dj-database-url` :
   
   ```python
   import dj_database_url
   
   # À la fin du fichier settings.py
   if 'DATABASE_URL' in os.environ:
       DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])
   ```
   
   Et ajouter à `requirements.txt` :
   ```
   dj-database-url==2.1.0
   ```

#### Option B : Utiliser SQLite (Simple mais limité)

SQLite fonctionne pour les tests, mais **n'est pas recommandé pour la production** car :
- Les fichiers sont effacés lors des redéploiements
- Pas adapté pour la concurrence

### Étape 7 : Exécuter les Migrations

1. Dans le dashboard Render, allez dans votre service
2. Ouvrez l'onglet **"Shell"**
3. Exécutez :
   ```bash
   python manage.py migrate
   ```

4. Créez un superutilisateur :
   ```bash
   python manage.py createsuperuser
   ```
   Suivez les instructions pour créer le compte admin.

### Étape 8 : Mettre à jour ALLOWED_HOSTS

Une fois le déploiement terminé :

1. Render vous donne une URL : `https://adplus-xxxx.onrender.com`
2. Allez dans les **"Environment Variables"** de votre service
3. Modifiez `ALLOWED_HOSTS` avec votre URL complète :
   ```
   adplus-xxxx.onrender.com
   ```
4. Cliquez sur **"Save Changes"** - Render redéploiera automatiquement

### Étape 9 : Vérifier le Déploiement

1. Visitez votre URL : `https://votre-service.onrender.com`
2. Vérifiez que la page d'accueil s'affiche
3. Testez la connexion admin
4. Vérifiez les logs en cas d'erreur

## 🔧 Configuration Avancée

### Personnaliser le Domaine

1. Dans les paramètres de votre service, section **"Custom Domains"**
2. Ajoutez votre domaine personnalisé
3. Suivez les instructions DNS fournies par Render

### Activer HTTPS

HTTPS est **automatiquement activé** sur Render pour tous les services.

### Configuration des Fichiers Statiques

WhiteNoise est déjà configuré dans `settings.py` pour servir les fichiers statiques.

### Monitoring et Logs

- **Logs** : Disponibles dans l'onglet "Logs" de votre service
- **Métriques** : Dashboard de monitoring automatique
- **Alertes** : Configurez des alertes pour les erreurs

## 🔄 Mises à jour

Pour mettre à jour votre application :

1. Faites vos modifications localement
2. Committez et pushez vers GitHub :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push origin main
   ```
3. Render détectera automatiquement les changements et redéploiera

## 🐛 Troubleshooting

### Erreur 500 (Internal Server Error)

1. **Vérifiez les logs** dans l'onglet "Logs"
2. **Vérifiez que `DEBUG=False`** est bien configuré
3. **Vérifiez que les migrations sont appliquées** : `python manage.py migrate`

### Fichiers statiques non chargés

1. Vérifiez que WhiteNoise est dans `MIDDLEWARE`
2. Exécutez `collectstatic` dans le build command
3. Vérifiez les logs pour les erreurs de fichiers manquants

### Erreur de base de données

1. Vérifiez que `DATABASE_URL` est bien configuré
2. Vérifiez que la base PostgreSQL est active dans Render
3. Exécutez les migrations : `python manage.py migrate`

### Erreur "DisallowedHost"

1. Vérifiez que `ALLOWED_HOSTS` contient votre URL Render
2. Mettez à jour la variable d'environnement
3. Attendez le redéploiement automatique

## 💰 Plans Render

- **Free Tier** : Parfait pour démarrer (avec limitations)
- **Starter** : $7/mois - Pour les applications en production
- **Standard** : À partir de $25/mois - Pour plus de ressources

## 📚 Ressources

- [Documentation Render](https://render.com/docs)
- [Déploiement Django sur Render](https://render.com/docs/deploy-django)
- [Guide PostgreSQL Render](https://render.com/docs/databases)

## ✅ Checklist de Déploiement

- [ ] Compte Render créé
- [ ] Web Service créé
- [ ] Variables d'environnement configurées (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- [ ] Base de données PostgreSQL créée (optionnel mais recommandé)
- [ ] Migrations exécutées
- [ ] Superutilisateur créé
- [ ] ALLOWED_HOSTS mis à jour avec l'URL Render
- [ ] Application accessible et fonctionnelle

---

**🎉 Félicitations ! Votre application AdPlus est maintenant déployée sur Render !**

Pour toute question, consultez les logs dans Render ou ouvrez une issue sur GitHub.

