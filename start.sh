#!/bin/bash
# Script de démarrage pour Render
# Exécute les migrations automatiquement puis démarre gunicorn

set -o errexit  # Arrêter en cas d'erreur

echo "🚀 Démarrage de l'application AdPlus..."

# Exécuter les migrations
echo "📦 Application des migrations de la base de données..."
# Essayer d'abord les migrations normales
if python manage.py migrate --noinput 2>&1 | grep -q "InconsistentMigrationHistory"; then
    echo "⚠️  Détection d'une incohérence dans l'historique des migrations..."
    echo "🔧 Correction de l'historique des migrations..."
    python manage.py fix_migrations --force || echo "⚠️  Échec de la correction, tentative avec --fake-initial..."
    python manage.py migrate --fake-initial --noinput || python manage.py migrate --noinput
else
    python manage.py migrate --noinput
fi

echo "✅ Migrations appliquées avec succès"

# Créer un superutilisateur si aucun n'existe et si les variables sont définies
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Création du superutilisateur..."
    python manage.py create_superuser_if_not_exists || echo "⚠️  Impossible de créer le superutilisateur"
else
    echo "ℹ️  DJANGO_SUPERUSER_PASSWORD non défini, pas de création automatique de superutilisateur"
fi

# Collecter les fichiers statiques (au cas où)
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput || echo "⚠️  Collectstatic a échoué mais on continue..."

echo "🌐 Démarrage de Gunicorn..."
# Démarrer Gunicorn avec le port fourni par Render
exec gunicorn plateforme_annonces.wsgi:application --bind 0.0.0.0:${PORT:-10000}

