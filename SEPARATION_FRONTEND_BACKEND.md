# 🚀 Guide de Séparation Frontend/Backend

Ce guide explique comment séparer le frontend du backend pour déployer le frontend sur Vercel (rapide, jamais en veille) et garder le backend Django sur Render (API uniquement).

## 📋 Architecture

```
Frontend (Vercel)          Backend (Render)
     │                            │
     │  HTTPS API Calls           │
     ├───────────────────────────>│
     │                            │
     │  JSON Responses            │
     │<───────────────────────────┤
     │                            │
   HTML/CSS/JS              Django REST API
   (Statique)               (PostgreSQL)
```

## 🎯 Objectifs

1. ✅ Backend Django sur Render (API REST uniquement)
2. ✅ Frontend HTML/CSS/JS sur Vercel (rapide, jamais en veille)
3. ✅ Communication via API REST (JSON)
4. ✅ Gestion du délai de réveil du backend (sleep plan gratuit)
5. ✅ UX professionnelle avec loaders et gestion d'erreurs

## 📁 Structure des Fichiers

```
projet/
├── backend/                    # Code Django (existant)
│   ├── annonces/
│   │   ├── api_views.py       # ViewSets API
│   │   ├── api_urls.py        # URLs API
│   │   └── serializers.py     # Serializers API
│   └── ...
│
└── frontend/                   # Frontend séparé (nouveau)
    ├── index.html             # Page portfolio (page publique)
    ├── app.html               # Application annonces
    ├── login.html             # Connexion
    ├── register.html          # Inscription
    ├── css/
    ├── js/
    │   ├── api.js             # Client API avec gestion erreurs
    │   └── app.js             # Logique application
    └── vercel.json            # Configuration Vercel
```

## 🔧 Configuration Backend (Django)

### 1. Endpoints API créés

- `GET /api/annonces/` - Liste des annonces
- `GET /api/annonces/{id}/` - Détail d'une annonce
- `POST /api/annonces/` - Créer une annonce (auth)
- `PUT/PATCH /api/annonces/{id}/` - Modifier (auth)
- `DELETE /api/annonces/{id}/` - Supprimer (auth)
- `POST /api/annonces/{id}/valider/` - Valider (admin)
- `POST /api/annonces/{id}/rejeter/` - Rejeter (admin)
- `GET /api/categories/` - Liste des catégories
- `POST /api/token/` - Authentification JWT
- `POST /api/token/refresh/` - Rafraîchir token

### 2. Configuration CORS

Les URLs Vercel doivent être ajoutées dans `CORS_ALLOWED_ORIGINS` sur Render :

```
CORS_ALLOWED_ORIGINS=https://votre-app.vercel.app,https://votre-app-git-main.vercel.app
```

### 3. Variables d'environnement Render

```
CORS_ALLOWED_ORIGINS=https://votre-frontend.vercel.app
```

## 📦 Configuration Frontend (Vercel)

### 1. Structure HTML/CSS/JS

Le frontend sera en HTML/CSS/JS pur, sans framework lourd.

### 2. Client API (`js/api.js`)

Gère :
- Appels API vers Render
- Gestion des tokens JWT
- Retry logic pour le réveil du backend
- Loaders et messages d'erreur

### 3. Configuration Vercel (`vercel.json`)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

## 🔐 Authentification

- JWT tokens stockés dans `localStorage`
- Refresh automatique des tokens
- Redirection vers login si token expiré

## ⚡ Gestion du Sleep Render

Le plan gratuit Render met l'application en veille après 15 min d'inactivité.

**Solution** :
1. Afficher un loader lors du premier appel
2. Retry automatique après 30-60 secondes
3. Message informatif : "Réveil du serveur en cours..."
4. Cache des données en localStorage pour affichage immédiat

## 📝 Prochaines Étapes

1. ✅ Créer les endpoints API (fait)
2. ⏳ Configurer CORS sur Render
3. ⏳ Créer la structure frontend
4. ⏳ Extraire portfolio.html
5. ⏳ Créer le client API
6. ⏳ Créer les pages frontend
7. ⏳ Configurer Vercel
8. ⏳ Tester et déployer

## 🔗 URLs

- **Backend API** : `https://gestion-annonce.onrender.com/api/`
- **Frontend** : `https://votre-app.vercel.app/` (à créer)

