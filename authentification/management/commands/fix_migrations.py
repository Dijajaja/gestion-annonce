"""
Commande Django pour corriger les migrations incohérentes.
Cette commande supprime les migrations problématiques de la table django_migrations
pour permettre une réinitialisation propre.
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Corrige les migrations incohérentes en supprimant les migrations problématiques de django_migrations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la suppression sans confirmation',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write(self.style.WARNING(
            '⚠️  Cette commande va supprimer certaines migrations de la table django_migrations.'
        ))
        self.stdout.write(self.style.WARNING(
            '⚠️  Cela permet de résoudre les erreurs "InconsistentMigrationHistory".'
        ))
        
        if not force:
            self.stdout.write(self.style.ERROR(
                'Utilisez --force pour confirmer cette opération.'
            ))
            return

        with connection.cursor() as cursor:
            # Supprimer les migrations de admin qui sont en conflit
            self.stdout.write('🗑️  Suppression des migrations admin problématiques...')
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = 'admin' AND name = '0001_initial'"
            )
            deleted_admin = cursor.rowcount
            
            # Supprimer les migrations de authentification si elles existent partiellement
            self.stdout.write('🗑️  Suppression des migrations authentification existantes...')
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = 'authentification'"
            )
            deleted_auth = cursor.rowcount
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ {deleted_admin} migration(s) admin supprimée(s)'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'✅ {deleted_auth} migration(s) authentification supprimée(s)'
            ))
            self.stdout.write(self.style.SUCCESS(
                '✅ Vous pouvez maintenant exécuter "python manage.py migrate"'
            ))

