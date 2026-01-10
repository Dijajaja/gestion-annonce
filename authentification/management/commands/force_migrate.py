"""
Commande Django pour forcer l'application de toutes les migrations.
Cette commande est plus robuste que migrate standard.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Force l\'application de toutes les migrations de manière robuste'

    def handle(self, *args, **options):
        self.stdout.write('📦 Application forcée de toutes les migrations...')
        
        # Vérifier la connexion à la base de données
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('✅ Connexion à la base de données OK'))
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur de connexion à la base de données: {e}'))
            return
        
        # Appliquer toutes les migrations
        try:
            call_command('migrate', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Migrations appliquées avec succès'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Erreur lors de migrate standard: {e}'))
            # Essayer avec fake-initial
            try:
                self.stdout.write('🔄 Tentative avec --fake-initial...')
                call_command('migrate', '--fake-initial', '--noinput', verbosity=2)
                self.stdout.write(self.style.SUCCESS('✅ Migrations appliquées avec --fake-initial'))
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f'❌ Échec même avec --fake-initial: {e2}'))
                raise

