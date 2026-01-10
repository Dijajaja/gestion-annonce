# 📦 Guide de Migration des Données vers Render

Ce guide vous explique comment transférer vos données locales (utilisateurs, catégories, annonces, images) vers votre base de données PostgreSQL sur Render.

## 📋 Ce qui sera migré

- ✅ **Utilisateurs** (avec leurs rôles admin/client)
- ✅ **Catégories** (nom, description, icône)
- ✅ **Annonces** (titre, description, prix, statut, etc.)
- ✅ **Images** des annonces (fichiers média)

## 🔧 Prérequis

1. Votre base de données locale doit être fonctionnelle
2. Vous devez avoir accès à votre `DATABASE_URL` PostgreSQL de Render
3. Python et pip installés localement

## 📤 Étape 1 : Exporter les données depuis votre base locale

### Option A : Utiliser Django dumpdata (Recommandé)

Cette méthode exporte toutes les données dans un fichier JSON.

1. **Ouvrez un terminal dans votre projet local**

2. **Activez votre environnement virtuel** (si vous en avez un)
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Exportez les données**
   ```bash
   python manage.py dumpdata authentification.Utilisateur annonces.Categorie annonces.Annonce --indent 2 --output data_export.json
   ```

4. **Vérifiez que le fichier `data_export.json` a été créé**

### Option B : Export SQL complet (Alternative)

Si vous utilisez SQLite localement :

1. **Localisez votre fichier `db.sqlite3`** (à la racine du projet)

2. **Exportez en SQL** (optionnel, pour sauvegarde)
   ```bash
   sqlite3 db.sqlite3 .dump > database_backup.sql
   ```

## 📁 Étape 2 : Exporter les fichiers média (Images)

Les images des annonces doivent aussi être transférées.

1. **Compressez le dossier `media`**
   
   **Windows (PowerShell)** :
   ```powershell
   Compress-Archive -Path media -DestinationPath media_backup.zip
   ```
   
   **macOS/Linux** :
   ```bash
   zip -r media_backup.zip media/
   ```

2. **Vérifiez que `media_backup.zip` a été créé**

## 📥 Étape 3 : Importer les données sur Render

### Méthode 1 : Via un script Python (Automatique - Recommandé)

Un script `import_data.py` a été créé pour faciliter l'import. Suivez ces étapes :

1. **Créez un fichier `.env` temporaire** à la racine de votre projet avec :
   ```env
   DATABASE_URL=votre_database_url_de_render
   ```

2. **Exécutez le script d'import**
   ```bash
   python import_data.py
   ```

### Méthode 2 : Import manuel via Django loaddata

Si Render vous permet d'accéder à un terminal (ou via votre machine locale connectée à la DB Render) :

1. **Récupérez votre `DATABASE_URL` de Render**
   - Allez dans votre base PostgreSQL sur Render
   - Copiez l'**"Internal Database URL"** ou **"External Database URL"**

2. **Configurez temporairement votre `.env` local** :
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

3. **Importez les données**
   ```bash
   python manage.py loaddata data_export.json
   ```

## 📤 Étape 4 : Uploader les fichiers média sur Render

Render ne permet pas facilement d'uploader des fichiers via l'interface. Voici les options :

### Option A : Upload via un script Django (Recommandé)

Un script `upload_media.py` sera créé pour uploader les images vers Render.

1. **Décompressez `media_backup.zip`**
   
   **Windows** :
   ```powershell
   Expand-Archive -Path media_backup.zip -DestinationPath .
   ```

2. **Modifiez temporairement `settings.py`** pour pointer vers la base Render :
   - Assurez-vous que `DATABASE_URL` dans `.env` pointe vers Render

3. **Exécutez le script** :
   ```bash
   python upload_media.py
   ```

### Option B : Upload manuel via l'interface (Limité)

Si vous avez peu d'images :
1. Connectez-vous à votre application sur Render
2. Créez de nouvelles annonces via l'interface admin
3. Uploader les images une par une

### Option C : Utiliser un service de stockage externe (Production)

Pour la production, considérez :
- **AWS S3**
- **Cloudinary** (gratuit pour petites quantités)
- **DigitalOcean Spaces**

## 🔍 Étape 5 : Vérification

Après l'import, vérifiez que tout est correct :

1. **Connectez-vous à votre application Render**
2. **Vérifiez dans l'admin** (`/admins/`) :
   - ✅ Les utilisateurs sont présents
   - ✅ Les catégories sont présentes
   - ✅ Les annonces sont présentes
   - ✅ Les images s'affichent correctement

## ⚠️ Notes importantes

1. **Les mots de passe** sont hashés, ils seront préservés lors de l'export/import Django.

2. **Les relations** (utilisateurs ↔ annonces, catégories ↔ annonces) seront automatiquement préservées.

3. **Si vous avez déjà des données sur Render**, l'import peut créer des doublons. Dans ce cas :
   - Videz d'abord les tables sur Render
   - Ou modifiez les IDs dans `data_export.json` avant l'import

4. **Les fichiers média** doivent être accessibles via le système de fichiers de Render. Le dossier `media` sera servi par WhiteNoise.

## 🐛 Résolution de problèmes

### Erreur : "Database connection failed"
- Vérifiez que `DATABASE_URL` est correct
- Vérifiez que votre IP est autorisée (pour External Database URL)

### Erreur : "IntegrityError: duplicate key value"
- Des données existent déjà sur Render
- Videz les tables ou utilisez `--natural-foreign` et `--natural-primary` lors du dump

### Les images ne s'affichent pas
- Vérifiez que le dossier `media` est bien présent sur Render
- Vérifiez que `MEDIA_ROOT` et `MEDIA_URL` sont correctement configurés dans `settings.py`

## 📝 Commandes rapides de référence

```bash
# Export
python manage.py dumpdata authentification.Utilisateur annonces.Categorie annonces.Annonce --indent 2 --output data_export.json

# Import
python manage.py loaddata data_export.json

# Export sans les relations (pour éviter les erreurs)
python manage.py dumpdata authentification.Utilisateur annonces.Categorie annonces.Annonce --natural-foreign --natural-primary --indent 2 --output data_export.json
```

## 🔄 Script automatique

Pour automatiser tout le processus, utilisez le script `migrate_to_render.py` qui sera créé dans le projet.

