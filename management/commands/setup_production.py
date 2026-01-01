from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from Structure.models import Cabinet, Forme_juridiques
from Adresse.models import commune, Ville, adresse
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Configuration initiale pour la production Railway'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Créer un superutilisateur',
        )
        parser.add_argument(
            '--setup-cabinet',
            action='store_true',
            help='Créer la structure de base du cabinet',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Configuration de production Railway')
        )

        if options['create_superuser']:
            self.create_superuser()

        if options['setup_cabinet']:
            self.setup_cabinet()

        self.stdout.write(
            self.style.SUCCESS('✅ Configuration terminée avec succès!')
        )

    def create_superuser(self):
        """Créer un superutilisateur si aucun n'existe"""
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('ADMIN_USERNAME', 'admin')
            email = os.environ.get('ADMIN_EMAIL', 'admin@cabinet.com')
            password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superutilisateur créé: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Un superutilisateur existe déjà')
            )

    @transaction.atomic
    def setup_cabinet(self):
        """Créer la structure de base du cabinet"""
        # Créer une forme juridique par défaut
        forme_juridique, created = Forme_juridiques.objects.get_or_create(
            nom="SARL",
            defaults={'nom': 'SARL'}
        )
        
        # Créer une ville par défaut
        ville, created = Ville.objects.get_or_create(
            nom="Kinshasa",
            defaults={'nom': 'Kinshasa'}
        )
        
        # Créer une commune par défaut
        commune_obj, created = commune.objects.get_or_create(
            nom="Gombe",
            defaults={'nom': 'Gombe', 'ville': ville}
        )
        
        # Créer une adresse par défaut
        adresse_obj, created = adresse.objects.get_or_create(
            numero="1",
            avenue="Avenue de la Justice",
            quartier="Centre-ville",
            commune=commune_obj,
            defaults={
                'numero': '1',
                'avenue': 'Avenue de la Justice',
                'quartier': 'Centre-ville',
                'commune': commune_obj
            }
        )
        
        # Créer un cabinet par défaut
        cabinet, created = Cabinet.objects.get_or_create(
            nom="Cabinet d'Avocats",
            defaults={
                'nom': "Cabinet d'Avocats",
                'numero_identification': 'CAB001',
                'telephone': '+243 000 000 000',
                'email': 'contact@cabinet.com',
                'forme_juridique': forme_juridique,
                'adresse': adresse_obj,
                'nom_fondateur': 'Maître Fondateur'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Cabinet créé avec succès')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Un cabinet existe déjà')
            )