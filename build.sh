#!/bin/bash
# Script de build pour Render

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques (en mode non-interactif et sans connexion DB si possible)
python manage.py collectstatic --noinput --clear || echo "Collectstatic a échoué mais on continue..."

