"""
Commande Django personnalisée pour créer un superutilisateur automatiquement
si aucun superutilisateur n'existe déjà.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée un superutilisateur si aucun n\'existe déjà'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
            help='Nom d\'utilisateur du superutilisateur',
        )
        parser.add_argument(
            '--email',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
            help='Email du superutilisateur',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', None),
            help='Mot de passe du superutilisateur',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Un superutilisateur existe déjà. Rien à faire.')
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Mot de passe non fourni. Utilisez --password ou définissez DJANGO_SUPERUSER_PASSWORD'
                )
            )
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Superutilisateur "{username}" créé avec succès !'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la création du superutilisateur : {e}')
            )

