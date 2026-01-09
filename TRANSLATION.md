# Guide de Traduction

## Configuration

La traduction est configurée pour supporter le français (par défaut) et l'anglais.

## Installation de gettext (pour générer les fichiers de traduction)

### Windows
1. Téléchargez gettext depuis : https://mlocati.github.io/articles/gettext-iconv-windows.html
2. Ajoutez le répertoire bin au PATH :
   - Trouvez où gettext est installé (généralement `C:\Program Files\gettext\bin` ou `C:\gettext\bin`)
   - Ajoutez ce chemin au PATH système :
     - Ouvrez "Variables d'environnement" dans Windows
     - Ajoutez le chemin dans "Path"
   - Ou temporairement dans PowerShell :
     ```powershell
     $env:PATH += ";C:\Program Files\gettext\bin"
     ```
3. Ou utilisez Chocolatey : `choco install gettext`

### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install gettext

# Mac
brew install gettext
```

## Génération des fichiers de traduction

Une fois gettext installé :

```bash
# Créer les fichiers de traduction pour l'anglais
python manage.py makemessages -l en

# Mettre à jour les traductions existantes
python manage.py makemessages -a

# Compiler les traductions
python manage.py compilemessages
```

## Utilisation

Le sélecteur de langue est disponible dans :
- Le header de la landing page
- La barre de navigation principale (base.html)

Les utilisateurs peuvent changer la langue en sélectionnant FR ou EN dans le menu déroulant.

## Traduction des chaînes de caractères

Pour traduire les textes de l'interface, utilisez le tag `{% trans %}` dans les templates :

```django
{% load i18n %}
{% trans "Texte à traduire" %}
```

Ou dans le code Python :

```python
from django.utils.translation import gettext as _
_("Texte à traduire")
```

## Fichiers de traduction

Les fichiers de traduction se trouvent dans :
- `locale/en/LC_MESSAGES/django.po` (anglais)
- `locale/fr/LC_MESSAGES/django.po` (français)

Après avoir modifié les fichiers .po, compilez-les avec :
```bash
python manage.py compilemessages
```

