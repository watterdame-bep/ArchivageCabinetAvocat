#!/usr/bin/env python
"""
Script de validation complète du déploiement Django + JSReport
"""
import requests
import os
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service

class DeploymentValidator:
    def __init__(self):
        self.results = []
        self.errors = []
        
    def log_result(self, test_name, success, message=""):
        """Enregistre le résultat d'un test"""
        status = "✅" if success else "❌"
        self.results.append(f"{status} {test_name}: {message}")
        if not success:
            self.errors.append(f"{test_name}: {message}")
    
    def test_django_config(self):
        """Teste la configuration Django"""
        print("🔧 Test de la configuration Django...")
        
        # Variables JSReport
        required_settings = [
            ('JSREPORT_URL', settings.JSREPORT_URL),
            ('JSREPORT_USERNAME', settings.JSREPORT_USERNAME),
            ('JSREPORT_PASSWORD', settings.JSREPORT_PASSWORD),
            ('JSREPORT_TIMEOUT', settings.JSREPORT_TIMEOUT)
        ]
        
        for setting_name, setting_value in required_settings:
            if setting_value:
                self.log_result(f"Config {setting_name}", True, f"Configuré: {setting_value}")
            else:
                self.log_result(f"Config {setting_name}", False, "Non configuré")
    
    def test_jsreport_connection(self):
        """Teste la connexion à JSReport"""
        print("🔗 Test de connexion JSReport...")
        
        try:
            # Test de ping
            if jsreport_service.test_connection():
                self.log_result("Connexion JSReport", True, f"Accessible: {settings.JSREPORT_URL}")
            else:
                self.log_result("Connexion JSReport", False, f"Inaccessible: {settings.JSREPORT_URL}")
                return False
            
            # Test d'authentification
            templates = jsreport_service.get_templates()
            if templates is not None:
                self.log_result("Authentification JSReport", True, f"{len(templates)} template(s) trouvé(s)")
                return templates
            else:
                self.log_result("Authentification JSReport", False, "Erreur d'authentification")
                return False
                
        except Exception as e:
            self.log_result("Connexion JSReport", False, str(e))
            return False
    
    def test_templates_availability(self, templates):
        """Teste la disponibilité des templates requis"""
        print("📋 Test des templates requis...")
        
        required_templates = [
            "Facture_paiement_client",
            "Extrait_de_compte_client", 
            "Facture_dossier",
            "Rapport"
        ]
        
        if not templates:
            for template in required_templates:
                self.log_result(f"Template {template}", False, "Templates non récupérés")
            return False
        
        template_names = [t.get('name', '') for t in templates]
        
        for template in required_templates:
            if template in template_names:
                self.log_result(f"Template {template}", True, "Disponible")
            else:
                self.log_result(f"Template {template}", False, "Manquant")
    
    def test_pdf_generation(self, templates):
        """Teste la génération de PDF"""
        print("📄 Test de génération PDF...")
        
        if not templates:
            self.log_result("Génération PDF", False, "Aucun template disponible")
            return
        
        # Données de test
        test_data = {
            "test": True,
            "title": "Test de Validation",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "message": "PDF généré lors de la validation du déploiement"
        }
        
        # Tester avec le premier template disponible
        template_name = templates[0].get('name', 'test')
        
        try:
            pdf_content = jsreport_service.generate_pdf(template_name, test_data)
            if pdf_content:
                size_kb = len(pdf_content) / 1024
                self.log_result("Génération PDF", True, f"Réussie ({size_kb:.1f} KB)")
            else:
                self.log_result("Génération PDF", False, "Contenu vide")
        except Exception as e:
            self.log_result("Génération PDF", False, str(e))
    
    def test_django_imports(self):
        """Teste les imports Django"""
        print("📦 Test des imports Django...")
        
        # Test des imports critiques
        imports_to_test = [
            ("utils.jsreport_service", "jsreport_service"),
            ("paiement.views", "imprimer_facture_paiement"),
            ("Dossier.views", "print_facture"),
            ("rapport.views", "generer_rapport_client")
        ]
        
        for module_name, function_name in imports_to_test:
            try:
                module = __import__(module_name, fromlist=[function_name])
                if hasattr(module, function_name):
                    self.log_result(f"Import {module_name}.{function_name}", True, "Disponible")
                else:
                    self.log_result(f"Import {module_name}.{function_name}", False, "Fonction non trouvée")
            except ImportError as e:
                self.log_result(f"Import {module_name}", False, str(e))
    
    def test_environment_variables(self):
        """Teste les variables d'environnement"""
        print("🌍 Test des variables d'environnement...")
        
        # Variables critiques
        env_vars = [
            'JSREPORT_URL',
            'JSREPORT_USERNAME', 
            'JSREPORT_PASSWORD'
        ]
        
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                # Masquer les mots de passe
                display_value = "***" if "PASSWORD" in var else value
                self.log_result(f"Env {var}", True, f"Définie: {display_value}")
            else:
                self.log_result(f"Env {var}", False, "Non définie")
    
    def run_full_validation(self):
        """Exécute la validation complète"""
        print("🧪 Validation Complète du Déploiement")
        print("=" * 60)
        
        # Tests séquentiels
        self.test_environment_variables()
        self.test_django_config()
        self.test_django_imports()
        
        templates = self.test_jsreport_connection()
        if templates:
            self.test_templates_availability(templates)
            self.test_pdf_generation(templates)
        
        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSULTATS DE LA VALIDATION")
        print("=" * 60)
        
        for result in self.results:
            print(result)
        
        # Statistiques
        total_tests = len(self.results)
        failed_tests = len(self.errors)
        success_tests = total_tests - failed_tests
        success_rate = (success_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 Statistiques:")
        print(f"   Total: {total_tests} tests")
        print(f"   Réussis: {success_tests}")
        print(f"   Échoués: {failed_tests}")
        print(f"   Taux de réussite: {success_rate:.1f}%")
        
        # Verdict final
        if failed_tests == 0:
            print("\n🎉 VALIDATION RÉUSSIE!")
            print("✅ Votre déploiement est opérationnel")
            return True
        else:
            print(f"\n⚠️ VALIDATION PARTIELLEMENT ÉCHOUÉE")
            print(f"❌ {failed_tests} problème(s) détecté(s)")
            print("\n🔧 Problèmes à corriger:")
            for error in self.errors:
                print(f"   • {error}")
            return False

def main():
    """Fonction principale"""
    validator = DeploymentValidator()
    success = validator.run_full_validation()
    
    if success:
        print("\n🚀 Votre application est prête pour la production!")
    else:
        print("\n🛠️ Corrigez les problèmes avant de continuer")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)