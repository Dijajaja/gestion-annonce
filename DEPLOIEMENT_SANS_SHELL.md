# 🚀 Déploiement sans accès Shell (Plan Gratuit Render)

Ce guide explique comment configurer votre application pour qu'elle s'initialise automatiquement sans avoir besoin d'accéder au Shell.

## ✅ Ce qui est maintenant automatique

Grâce au script `start.sh`, votre application va :
1. ✅ Appliquer automatiquement les migrations au démarrage
2. ✅ Créer un superutilisateur automatiquement (si configuré)
3. ✅ Collecter les fichiers statiques
4. ✅ Démarrer Gunicorn

## 🔧 Configuration sur Render

### Étape 1 : Mettre à jour le Start Command

Dans votre Web Service Render :

1. Allez dans **"Settings"** → **"Build & Deploy"**
2. Cherchez le champ **"Start Command"**
3. Remplacez le contenu par :
   ```bash
   chmod +x start.sh && ./start.sh
   ```
4. Sauvegardez

### Étape 2 : Ajouter les Variables d'Environnement pour le Superutilisateur

Dans **"Environment"** de votre Web Service, ajoutez ces variables **optionnelles** si vous voulez créer automatiquement un superutilisateur :

#### Option A : Création automatique du superutilisateur

1. **DJANGO_SUPERUSER_USERNAME**
   - Key: `DJANGO_SUPERUSER_USERNAME`
   - Value: `admin` (ou le nom d'utilisateur de votre choix)

2. **DJANGO_SUPERUSER_EMAIL**
   - Key: `DJANGO_SUPERUSER_EMAIL`
   - Value: `admin@example.com` (ou votre email)

3. **DJANGO_SUPERUSER_PASSWORD**
   - Key: `DJANGO_SUPERUSER_PASSWORD`
   - Value: `VotreMotDePasseSecurise123!` (choisissez un mot de passe fort)

⚠️ **Important** : Ces variables sont **optionnelles**. Si vous ne les définissez pas, le superutilisateur ne sera pas créé automatiquement. Vous pourrez toujours vous inscrire via l'interface et changer votre rôle en base de données plus tard, ou attendre d'avoir accès à un Shell.

#### Option B : Pas de création automatique

Si vous ne définissez pas ces variables, l'application fonctionnera normalement, mais vous devrez créer votre compte admin autrement :
- Soit via l'interface d'inscription puis modifier le rôle en base de données
- Soit attendre d'avoir accès à un Shell (si vous passez à un plan payant)

### Étape 3 : Variables obligatoires (à définir de toute façon)

Assurez-vous d'avoir ces variables :

1. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: *(générez une clé sécurisée avec la commande dans le guide)*

3. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `votre-service.onrender.com` (votre URL Render, sans https://)

4. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: *(l'URL de votre base de données PostgreSQL Render)*

### Étape 4 : Redéployer

1. Dans Render, allez dans **"Manual Deploy"**
2. Cliquez sur **"Clear build cache & deploy"**
3. Attendez la fin du build (5-10 minutes)

## 🎯 Après le déploiement

1. ✅ Les migrations seront appliquées automatiquement
2. ✅ Si vous avez configuré les variables de superutilisateur, celui-ci sera créé
3. ✅ Votre application sera accessible sur votre URL Render

## 🔐 Se connecter en tant qu'administrateur

### Si vous avez configuré la création automatique :

- URL de connexion : `https://votre-service.onrender.com/admins/`
- Username : *(celui défini dans `DJANGO_SUPERUSER_USERNAME`)*
- Password : *(celui défini dans `DJANGO_SUPERUSER_PASSWORD`)*

### Si vous n'avez pas configuré la création automatique :

Vous pouvez :
1. Vous inscrire via l'interface (`/inscription/`)
2. Attendre d'avoir un accès Shell pour créer un superutilisateur
3. Ou modifier directement en base de données (si vous avez accès)

## 🐛 Vérifier les logs

Pour vérifier que tout s'est bien passé :

1. Allez dans **"Logs"** de votre Web Service
2. Cherchez ces messages :
   - ✅ `✅ Migrations appliquées avec succès`
   - ✅ `✅ Superutilisateur "admin" créé avec succès !` (si configuré)
   - ✅ `🌐 Démarrage de Gunicorn...`

## ⚠️ Problèmes courants

### Les migrations ne s'appliquent pas

Vérifiez dans les logs s'il y a une erreur. Assurez-vous que `DATABASE_URL` est bien configuré.

### Le superutilisateur n'est pas créé

- Vérifiez que toutes les variables (`DJANGO_SUPERUSER_*`) sont bien définies
- Vérifiez les logs pour voir s'il y a une erreur
- Si un superutilisateur existe déjà, il ne sera pas recréé (c'est normal)

### L'application ne démarre pas

- Vérifiez les logs pour voir l'erreur exacte
- Assurez-vous que toutes les variables obligatoires sont définies
- Vérifiez que `ALLOWED_HOSTS` contient votre URL Render

