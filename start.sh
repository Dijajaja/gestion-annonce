#!/bin/bash
# Script de démarrage pour Render
# Exécute les migrations automatiquement puis démarre gunicorn

set +o errexit  # Ne pas arrêter immédiatement en cas d'erreur pour gérer les migrations

echo "🚀 Démarrage de l'application AdPlus..."

# Exécuter les migrations
echo "📦 Application des migrations de la base de données..."
# Essayer d'abord les migrations normales
MIGRATE_OUTPUT=$(python manage.py migrate --noinput 2>&1)
MIGRATE_EXIT_CODE=$?

if [ $MIGRATE_EXIT_CODE -ne 0 ]; then
    echo "$MIGRATE_OUTPUT"
    if echo "$MIGRATE_OUTPUT" | grep -q "InconsistentMigrationHistory" || echo "$MIGRATE_OUTPUT" | grep -q "admin.0001_initial"; then
        echo "⚠️  Détection d'une incohérence dans l'historique des migrations..."
        echo "🔧 Correction de l'historique des migrations..."
        python manage.py fix_migrations --force || echo "⚠️  Échec de la correction"
        echo "🔄 Nouvelle tentative d'application des migrations..."
        python manage.py migrate --fake-initial --noinput || python manage.py migrate --noinput
    else
        echo "❌ Erreur lors des migrations (non liée à InconsistentMigrationHistory)"
        exit 1
    fi
else
    echo "$MIGRATE_OUTPUT"
fi

echo "✅ Migrations appliquées avec succès"

# Réactiver errexit pour le reste du script
set -o errexit

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

