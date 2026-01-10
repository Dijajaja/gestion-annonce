# 🔧 Correction de l'erreur ALLOWED_HOSTS

## Problème

L'erreur suivante apparaît :
```
django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'gestion-annonce.onrender.com'. 
You may need to add 'gestion-annonce.onrender.com' to ALLOWED_HOSTS.
```

## Solution automatique (Recommandé)

Le code a été modifié pour **détecter automatiquement** si vous êtes sur Render et ajouter votre domaine automatiquement.

Cependant, pour une configuration explicite, ajoutez la variable d'environnement suivante sur Render :

## Configuration sur Render

### Option 1 : Via variable d'environnement (Recommandé)

1. Allez dans votre **Web Service** sur Render
2. Cliquez sur **"Environment"**
3. Cliquez sur **"Add Environment Variable"**
4. Ajoutez :
   - **Key** : `ALLOWED_HOSTS`
   - **Value** : `gestion-annonce.onrender.com`
5. Cliquez sur **"Save Changes"**
6. Redéployez votre service

### Option 2 : Via RENDER_EXTERNAL_URL (Automatique)

Render définit automatiquement `RENDER_EXTERNAL_URL`. Si cette variable est détectée, le domaine sera ajouté automatiquement.

### Option 3 : Multiple domaines

Si vous avez plusieurs domaines, séparez-les par des virgules :
```
gestion-annonce.onrender.com,votre-domaine.com,www.votre-domaine.com
```

## Vérification

Après avoir ajouté la variable et redéployé :

1. ✅ L'erreur `DisallowedHost` ne devrait plus apparaître
2. ✅ Votre site devrait être accessible sur `https://gestion-annonce.onrender.com`
3. ✅ Vérifiez les logs - ils ne devraient plus contenir d'erreurs `DisallowedHost`

## Note

La solution automatique devrait fonctionner, mais si vous rencontrez encore des problèmes, utilisez l'Option 1 pour définir explicitement `ALLOWED_HOSTS`.

