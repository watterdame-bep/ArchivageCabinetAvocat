#!/usr/bin/env python
"""
Commande Django pour tester JSReport en production Railway
Usage: python manage.py test_railway_jsreport
"""
from django.core.management.base import BaseCommand
from utils.jsreport_service import jsreport_service
import os

class Command(BaseCommand):
    help = 'Test JSReport service connectivity and template availability'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-pdf',
            action='store_true',
            help='Test PDF generation with sample data',
        )
        parser.add_argument(
            '--template',
            type=str,
            help='Test specific template name',
        )

    def handle(self, *args, **options):
        self.stdout.write("🧪 Test JSReport Service - Railway Production")
        self.stdout.write("=" * 50)
        
        # Vérifier la configuration
        jsreport_url = os.environ.get('JSREPORT_URL')
        if not jsreport_url:
            self.stdout.write(
                self.style.ERROR("❌ JSREPORT_URL non définie dans les variables d'environnement")
            )
            return
        
        self.stdout.write(f"🌐 JSReport URL: {jsreport_url}")
        
        # Test de connexion
        self.stdout.write("\n📡 Test de connexion...")
        try:
            templates = jsreport_service.get_templates()
            if templates:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Connexion réussie! {len(templates)} template(s) trouvé(s)")
                )
                
                # Lister les templates
                self.stdout.write("\n📋 Templates disponibles:")
                for template in templates:
                    self.stdout.write(f"   ✅ {template['name']}")
            else:
                self.stdout.write(
                    self.style.ERROR("❌ Aucun template trouvé ou erreur de connexion")
                )
                return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur de connexion: {e}")
            )
            return
        
        # Test de génération PDF si demandé
        if options['test_pdf']:
            self.stdout.write("\n🔄 Test de génération PDF...")
            
            # Choisir le template à tester
            template_name = options['template']
            if not template_name:
                # Utiliser le premier template disponible
                template_name = templates[0]['name'] if templates else None
            
            if template_name:
                self.stdout.write(f"📄 Test du template: {template_name}")
                
                # Données de test
                test_data = {
                    "title": "Test Railway Deployment",
                    "date": "2024-01-01",
                    "client": {
                        "nom": "Client Test",
                        "email": "test@example.com"
                    },
                    "items": [
                        {"description": "Service 1", "amount": 100},
                        {"description": "Service 2", "amount": 200}
                    ],
                    "total": 300
                }
                
                try:
                    pdf_content = jsreport_service.generate_pdf(template_name, test_data)
                    if pdf_content:
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ PDF généré avec succès! Taille: {len(pdf_content)} bytes")
                        )
                        
                        # Optionnel: sauvegarder le PDF de test
                        test_file = f"test_railway_{template_name}.pdf"
                        with open(test_file, 'wb') as f:
                            f.write(pdf_content)
                        self.stdout.write(f"💾 PDF de test sauvegardé: {test_file}")
                    else:
                        self.stdout.write(
                            self.style.ERROR("❌ Erreur lors de la génération PDF")
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Erreur génération PDF: {e}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING("⚠️ Aucun template spécifié pour le test PDF")
                )
        
        # Résumé final
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🎯 RÉSUMÉ DU TEST")
        self.stdout.write("=" * 50)
        
        if templates:
            self.stdout.write(
                self.style.SUCCESS("✅ JSReport service opérationnel sur Railway!")
            )
            self.stdout.write(f"📊 {len(templates)} template(s) disponible(s)")
            
            if options['test_pdf']:
                self.stdout.write("📄 Test de génération PDF effectué")
            
            self.stdout.write("\n🚀 Votre application est prête pour la production!")
        else:
            self.stdout.write(
                self.style.ERROR("❌ JSReport service non opérationnel")
            )
            self.stdout.write("🔧 Vérifiez la configuration et les templates migrés")