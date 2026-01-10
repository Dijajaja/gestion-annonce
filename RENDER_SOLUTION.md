# 🔧 Solution : Erreur "cannot have more than one active free tier database"

## Problème
Render ne permet qu'**une seule base de données PostgreSQL gratuite** par compte.

## ✅ Solutions

### Solution 1 : Réutiliser la base existante (RECOMMANDÉ)

1. **Trouver votre base existante** :
   - Dans le dashboard Render, allez dans la section **"Databases"**
   - Vous verrez votre base PostgreSQL existante

2. **Récupérer l'URL de la base** :
   - Cliquez sur votre base PostgreSQL
   - Allez dans l'onglet **"Info"** ou **"Connections"**
   - Copiez l'**"Internal Database URL"** (pour Render) ou **"External Database URL"** (si vous voulez y accéder depuis l'extérieur)
   - Format : `postgresql://user:password@host:port/dbname`

3. **Ajouter DATABASE_URL à votre Web Service** :
   - Allez dans votre Web Service (celui que vous créez pour AdPlus)
   - Section **"Environment"** → **"Environment Variables"**
   - Cliquez sur **"Add Environment Variable"**
   - Key : `DATABASE_URL`
   - Value : Collez l'URL que vous avez copiée
   - Cliquez sur **"Save Changes"**

4. **Important** : Si vous utilisez plusieurs services avec la même base, c'est possible ! Ils peuvent partager la même base PostgreSQL.

### Solution 2 : Supprimer l'ancienne base (si vous n'en avez plus besoin)

⚠️ **ATTENTION** : Cette action supprime définitivement toutes les données !

1. Dans le dashboard Render, section **"Databases"**
2. Cliquez sur la base que vous voulez supprimer
3. Allez dans **"Settings"** (en bas de la page)
4. Scroll jusqu'à **"Delete Database"**
5. Confirmez la suppression
6. Maintenant vous pouvez créer une nouvelle base

### Solution 3 : Utiliser SQLite temporairement (Pour tester seulement)

Si vous voulez juste tester le déploiement sans base PostgreSQL :

1. **Ne créez PAS de base PostgreSQL** sur Render
2. Votre application utilisera SQLite automatiquement
3. ⚠️ **Limitations** :
   - Les données seront perdues lors des redéploiements
   - Pas adapté pour la production
   - Limité en performance

### Solution 4 : Passer à un plan payant

Si vous avez besoin de plusieurs bases de données :
- Plan **Starter** : $7/mois (une base incluse, mais peut en ajouter plus)
- Plan **Standard** : $25/mois (plus de ressources)

## 🎯 Solution Recommandée pour Votre Cas

**Utilisez votre base PostgreSQL existante** :

1. Allez dans votre base PostgreSQL existante sur Render
2. Copiez l'**"Internal Database URL"**
3. Dans votre Web Service AdPlus → Environment Variables
4. Ajoutez : `DATABASE_URL` = l'URL copiée
5. Votre application utilisera cette base

**Avantages** :
- ✅ Pas besoin de créer une nouvelle base
- ✅ Pas de frais supplémentaires
- ✅ Toutes vos données au même endroit
- ✅ Vous pouvez utiliser plusieurs services avec la même base

## 📝 Exemple de Configuration

Dans votre Web Service, vous devriez avoir ces variables :

```
DEBUG=False
SECRET_KEY=votre_secret_key_ici
ALLOWED_HOSTS=votre-service.onrender.com
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 🔍 Vérification

Pour vérifier que tout fonctionne :

1. Après avoir ajouté `DATABASE_URL`, allez dans l'onglet **"Shell"** de votre Web Service
2. Exécutez :
   ```bash
   python manage.py migrate
   ```
3. Si ça fonctionne, votre base est bien connectée !

---

**Besoin d'aide ?** Vérifiez les logs de votre service dans Render pour voir les erreurs spécifiques.

