# 🚀 Déploiement du Frontend sur Vercel

## Préparation

Les fichiers frontend sont dans le dossier `frontend/`. 

## Déploiement via Vercel CLI

1. **Installer Vercel CLI** :
   ```bash
   npm i -g vercel
   ```

2. **Se connecter** :
   ```bash
   vercel login
   ```

3. **Déployer** :
   ```bash
   cd frontend
   vercel
   ```

## Déploiement via GitHub

1. **Créer un dépôt séparé pour le frontend** (recommandé)
   - Créer un nouveau dépôt GitHub
   - Copier le dossier `frontend/` dans ce dépôt

2. **Connecter à Vercel** :
   - Aller sur [vercel.com](https://vercel.com)
   - "New Project"
   - Importer le dépôt GitHub
   - Vercel détectera automatiquement les fichiers statiques

## Configuration CORS sur Render

Après avoir l'URL Vercel, ajoutez-la dans Render :

**Variables d'environnement** :
- Key: `CORS_ALLOWED_ORIGINS`
- Value: `https://votre-app.vercel.app,https://votre-app-git-main.vercel.app`

## URLs

- **Frontend** : `https://votre-app.vercel.app/`
- **Backend API** : `https://gestion-annonce.onrender.com/api/`

