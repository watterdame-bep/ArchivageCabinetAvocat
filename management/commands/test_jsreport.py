"""
Commande Django pour tester la connexion JSReport
Usage: python manage.py test_jsreport
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.jsreport_service import jsreport_service
import json

class Command(BaseCommand):
    help = 'Teste la connexion et la configuration JSReport'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Affichage détaillé des informations',
        )
        parser.add_argument(
            '--test-pdf',
            action='store_true',
            help='Teste la génération d\'un PDF simple',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Test de la configuration JSReport')
        )
        self.stdout.write('=' * 50)
        
        # Afficher la configuration
        self.stdout.write(f"📍 URL JSReport: {settings.JSREPORT_URL}")
        self.stdout.write(f"👤 Utilisateur: {settings.JSREPORT_USERNAME}")
        self.stdout.write(f"🔒 Mot de passe: {'***' if settings.JSREPORT_PASSWORD else 'Non configuré'}")
        self.stdout.write(f"⏱️  Timeout: {settings.JSREPORT_TIMEOUT}s")
        self.stdout.write('')
        
        # Test de connexion
        self.stdout.write("🔗 Test de connexion...")
        if jsreport_service.test_connection():
            self.stdout.write(
                self.style.SUCCESS("✅ Connexion JSReport réussie!")
            )
        else:
            self.stdout.write(
                self.style.ERROR("❌ Impossible de se connecter à JSReport")
            )
            self.stdout.write("Vérifiez :")
            self.stdout.write("- L'URL JSReport est correcte")
            self.stdout.write("- Le service JSReport est démarré")
            self.stdout.write("- Les credentials sont corrects")
            return
        
        # Lister les templates
        self.stdout.write("\n📋 Templates disponibles...")
        templates = jsreport_service.get_templates()
        if templates:
            self.stdout.write(f"Trouvé {len(templates)} template(s):")
            for template in templates:
                name = template.get('name', 'Sans nom')
                engine = template.get('engine', 'Inconnu')
                self.stdout.write(f"  - {name} ({engine})")
        else:
            self.stdout.write(
                self.style.WARNING("⚠️  Aucun template trouvé ou erreur d'accès")
            )
        
        # Test de génération PDF si demandé
        if options['test_pdf']:
            self.stdout.write("\n📄 Test de génération PDF...")
            test_data = {
                "title": "Test PDF",
                "content": "Ceci est un test de génération PDF depuis Django",
                "date": "2024-01-01",
                "items": [
                    {"name": "Item 1", "value": "100"},
                    {"name": "Item 2", "value": "200"}
                ]
            }
            
            # Utiliser le premier template disponible ou un template par défaut
            template_name = "test"  # Changez selon vos templates
            if templates and len(templates) > 0:
                template_name = templates[0].get('name', 'test')
            
            pdf_content = jsreport_service.generate_pdf(template_name, test_data)
            if pdf_content:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ PDF généré avec succès! Taille: {len(pdf_content)} bytes")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Erreur lors de la génération du PDF avec le template '{template_name}'")
                )
        
        # Informations détaillées si demandées
        if options['verbose']:
            self.stdout.write("\n🔍 Informations détaillées:")
            self.stdout.write(f"Service JSReport: {jsreport_service.__class__.__name__}")
            self.stdout.write(f"URL API: {jsreport_service.api_url}")
            self.stdout.write(f"Authentification: {'Activée' if jsreport_service.username else 'Désactivée'}")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS("🎯 Test terminé!")
        )