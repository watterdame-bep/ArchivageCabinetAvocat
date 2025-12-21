#!/usr/bin/env python
"""
Script de diagnostic JSReport pour identifier les problèmes d'impression des factures
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service
from paiement.models import Paiement

class JSReportDiagnostic:
    def __init__(self):
        self.jsreport_url = getattr(settings, 'JSREPORT_URL', 'http://localhost:5488')
        self.username = getattr(settings, 'JSREPORT_USERNAME', 'admin')
        self.password = getattr(settings, 'JSREPORT_PASSWORD', 'admin123')
        self.timeout = getattr(settings, 'JSREPORT_TIMEOUT', 60)
        
    def print_config(self):
        """Affiche la configuration JSReport actuelle"""
        print("🔧 CONFIGURATION JSREPORT")
        print("=" * 50)
        print(f"URL JSReport: {self.jsreport_url}")
        print(f"Username: {self.username}")
        print(f"Password: {'*' * len(self.password) if self.password else 'NON DÉFINI'}")
        print(f"Timeout: {self.timeout}s")
        print()
        
    def test_docker_container(self):
        """Vérifie si le conteneur Docker JSReport est en cours d'exécution"""
        print("🐳 VÉRIFICATION CONTENEUR DOCKER")
        print("=" * 50)
        
        try:
            import subprocess
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            
            if 'jsreport' in result.stdout.lower():
                print("✅ Conteneur JSReport trouvé dans Docker")
                # Extraire les informations du conteneur
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'jsreport' in line.lower():
                        print(f"   📋 {line}")
            else:
                print("❌ Aucun conteneur JSReport trouvé")
                print("💡 Vérifiez que JSReport est démarré avec:")
                print("   docker-compose -f docker-compose.jsreport.yml up -d")
                
        except FileNotFoundError:
            print("❌ Docker n'est pas installé ou accessible")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification Docker: {e}")
        print()
        
    def test_connection(self):
        """Teste la connexion de base à JSReport"""
        print("🔗 TEST DE CONNEXION")
        print("=" * 50)
        
        try:
            ping_url = f"{self.jsreport_url}/api/ping"
            print(f"Test de ping: {ping_url}")
            
            response = requests.get(ping_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ JSReport est accessible")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
            else:
                print(f"❌ JSReport non accessible (Status: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            print("❌ Impossible de se connecter à JSReport")
            print("💡 Vérifiez que:")
            print("   - JSReport est démarré")
            print("   - L'URL est correcte")
            print("   - Le port 5488 est ouvert")
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
        print()
        
    def test_authentication(self):
        """Teste l'authentification JSReport"""
        print("🔐 TEST D'AUTHENTIFICATION")
        print("=" * 50)
        
        try:
            templates_url = f"{self.jsreport_url}/odata/templates"
            print(f"Test d'authentification: {templates_url}")
            
            response = requests.get(
                templates_url,
                auth=(self.username, self.password),
                timeout=10
            )
            
            if response.status_code == 200:
                templates = response.json().get('value', [])
                print(f"✅ Authentification réussie")
                print(f"   Nombre de templates: {len(templates)}")
                
                # Lister les templates
                if templates:
                    print("   📋 Templates disponibles:")
                    for template in templates:
                        print(f"      - {template.get('name', 'Sans nom')}")
                else:
                    print("   ⚠️ Aucun template trouvé")
                    
            elif response.status_code == 401:
                print("❌ Erreur d'authentification")
                print("💡 Vérifiez le nom d'utilisateur et mot de passe")
            else:
                print(f"❌ Erreur d'authentification (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
        print()
        
    def test_service_class(self):
        """Teste la classe JSReportService"""
        print("🛠️ TEST DE LA CLASSE SERVICE")
        print("=" * 50)
        
        try:
            # Test de connexion via le service
            connection_ok = jsreport_service.test_connection()
            print(f"Connexion via service: {'✅ OK' if connection_ok else '❌ ÉCHEC'}")
            
            # Test de récupération des templates
            templates = jsreport_service.get_templates()
            if templates is not None:
                print(f"✅ Templates récupérés: {len(templates)}")
                
                # Vérifier les templates requis
                required_templates = [
                    "Facture_paiement_client",
                    "Facture_dossier", 
                    "Extrait_de_compte_client"
                ]
                
                template_names = [t.get('name', '') for t in templates]
                
                for required in required_templates:
                    if required in template_names:
                        print(f"   ✅ Template '{required}' trouvé")
                    else:
                        print(f"   ❌ Template '{required}' MANQUANT")
            else:
                print("❌ Impossible de récupérer les templates")
                
        except Exception as e:
            print(f"❌ Erreur du service: {e}")
        print()
        
    def test_pdf_generation(self):
        """Teste la génération d'un PDF simple"""
        print("📄 TEST DE GÉNÉRATION PDF")
        print("=" * 50)
        
        try:
            # Données de test simples
            test_data = {
                "test": True,
                "date": datetime.now().strftime("%d/%m/%Y"),
                "message": "Test de génération PDF"
            }
            
            # Essayer de générer un PDF avec un template simple
            print("Tentative de génération PDF de test...")
            
            pdf_content = jsreport_service.generate_pdf(
                template_name="Facture_paiement_client",  # Template principal
                data=test_data
            )
            
            if pdf_content:
                size_kb = len(pdf_content) / 1024
                print(f"✅ PDF généré avec succès")
                print(f"   Taille: {size_kb:.2f} KB")
                
                # Sauvegarder le PDF de test
                with open('test_jsreport.pdf', 'wb') as f:
                    f.write(pdf_content)
                print("   📁 PDF sauvegardé: test_jsreport.pdf")
            else:
                print("❌ Échec de génération PDF")
                
        except Exception as e:
            print(f"❌ Erreur de génération PDF: {e}")
        print()
        
    def test_real_invoice(self):
        """Teste avec une vraie facture si disponible"""
        print("🧾 TEST AVEC VRAIE FACTURE")
        print("=" * 50)
        
        try:
            # Chercher un paiement récent
            paiement = Paiement.objects.filter(
                dossier__isnull=False
            ).first()
            
            if not paiement:
                print("⚠️ Aucun paiement trouvé pour tester")
                return
                
            print(f"Test avec paiement ID: {paiement.id}")
            print(f"Dossier: {paiement.dossier.numero_reference_dossier}")
            
            # Préparer les données comme dans la vraie vue
            data = {
                "paiement": {
                    "today": datetime.now().strftime("%d/%m/%Y"),
                    "date": paiement.date_paiement.strftime("%d/%m/%Y %H:%M"),
                    "type_paiement": str(paiement.type_paiement or ''),
                    "personne_qui_paie": str(paiement.personne_qui_paie or ''),
                    "notes": str(paiement.notes or ''),
                    "montant_USD": float(paiement.montant_payer_dollars or 0),
                    "montant_CDF": float(paiement.montant_payer_fc or 0),
                },
                "dossier": {
                    "numero_dossier": str(paiement.dossier.numero_reference_dossier),
                    "num_facture": str(paiement.dossier.reference or ''),
                },
                "client": {
                    "nom": str(paiement.client.nom if paiement.client else ''),
                    "prenom": str(paiement.client.prenom if paiement.client else ''),
                }
            }
            
            pdf_content = jsreport_service.generate_pdf(
                template_name="Facture_paiement_client",
                data=data
            )
            
            if pdf_content:
                size_kb = len(pdf_content) / 1024
                print(f"✅ Facture réelle générée avec succès")
                print(f"   Taille: {size_kb:.2f} KB")
                
                # Sauvegarder la facture
                filename = f"facture_test_{paiement.id}.pdf"
                with open(filename, 'wb') as f:
                    f.write(pdf_content)
                print(f"   📁 Facture sauvegardée: {filename}")
            else:
                print("❌ Échec de génération de la facture réelle")
                
        except Exception as e:
            print(f"❌ Erreur avec vraie facture: {e}")
        print()
        
    def run_full_diagnostic(self):
        """Lance le diagnostic complet"""
        print("🚀 DIAGNOSTIC JSREPORT COMPLET")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        
        self.print_config()
        self.test_docker_container()
        self.test_connection()
        self.test_authentication()
        self.test_service_class()
        self.test_pdf_generation()
        self.test_real_invoice()
        
        print("🏁 DIAGNOSTIC TERMINÉ")
        print("=" * 60)

if __name__ == "__main__":
    diagnostic = JSReportDiagnostic()
    diagnostic.run_full_diagnostic()