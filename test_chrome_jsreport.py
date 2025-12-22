#!/usr/bin/env python
"""
Test de la configuration Chrome pour JSReport Railway
"""
import os
import sys
import django
import requests
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service

def test_chrome_config_files():
    """Teste que les fichiers Chrome sont présents"""
    print("📁 TEST FICHIERS CHROME")
    print("=" * 40)
    
    # Vérifier Dockerfile avec Chrome
    dockerfile_chrome = "Dockerfile.jsreport.chrome"
    if os.path.exists(dockerfile_chrome):
        print(f"✅ {dockerfile_chrome} trouvé")
        
        with open(dockerfile_chrome, 'r') as f:
            content = f.read()
        
        chrome_checks = [
            ("Installation Chrome", "google-chrome-stable" in content),
            ("Variables Puppeteer", "PUPPETEER_EXECUTABLE_PATH" in content),
            ("Arguments no-sandbox", "--no-sandbox" in content),
            ("USER root", "USER root" in content),
            ("USER jsreport", "USER jsreport" in content)
        ]
        
        print("📋 Vérifications Dockerfile Chrome:")
        for check_name, result in chrome_checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            
        all_good = all(result for _, result in chrome_checks)
        
        if all_good:
            print("🎉 Dockerfile Chrome parfait !")
            return True
        else:
            print("⚠️ Quelques éléments à corriger")
            return False
    else:
        print(f"❌ {dockerfile_chrome} manquant")
        return False

def test_chrome_config_json():
    """Teste la configuration JSON pour Chrome"""
    print("\n📄 TEST CONFIGURATION CHROME JSON")
    print("=" * 40)
    
    config_chrome = "jsreport.config.chrome.json"
    if os.path.exists(config_chrome):
        print(f"✅ {config_chrome} trouvé")
        
        try:
            with open(config_chrome, 'r') as f:
                config = json.load(f)
            
            chrome_checks = [
                ("chrome-pdf enabled", config.get("extensions", {}).get("chrome-pdf", {}).get("enabled") == True),
                ("executablePath", "/usr/bin/google-chrome" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("executablePath", ""))),
                ("--no-sandbox", "--no-sandbox" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("launchOptions", {}).get("args", []))),
                ("--disable-dev-shm-usage", "--disable-dev-shm-usage" in str(config.get("extensions", {}).get("chrome-pdf", {}).get("launchOptions", {}).get("args", []))),
                ("timeout configuré", config.get("extensions", {}).get("chrome-pdf", {}).get("timeout", 0) >= 120000)
            ]
            
            print("📋 Vérifications config Chrome:")
            for check_name, result in chrome_checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                
            all_good = all(result for _, result in chrome_checks)
            
            if all_good:
                print("🎉 Configuration Chrome parfaite !")
                return True
            else:
                print("⚠️ Quelques éléments à corriger")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            return False
    else:
        print(f"❌ {config_chrome} manquant")
        return False

def test_jsreport_connection_chrome():
    """Teste la connexion JSReport avec Chrome"""
    print("\n🔗 TEST CONNEXION JSREPORT CHROME")
    print("=" * 40)
    
    jsreport_url = getattr(settings, 'JSREPORT_URL', 'http://localhost:5488')
    
    if 'localhost' in jsreport_url:
        print("⚠️ URL JSReport pointe vers localhost")
        print("   Impossible de tester Chrome sur Railway depuis local")
        return None
    
    try:
        # Test de connexion de base
        if jsreport_service.test_connection():
            print("✅ JSReport accessible")
            
            # Test de génération PDF simple
            test_data = {
                "test": "Chrome PDF Generation",
                "date": "2025-12-21",
                "message": "Test génération PDF avec Chrome"
            }
            
            print("🔄 Test génération PDF avec Chrome...")
            
            pdf_content = jsreport_service.generate_pdf(
                template_name="Facture_paiement_client",
                data=test_data
            )
            
            if pdf_content:
                size_kb = len(pdf_content) / 1024
                print(f"✅ PDF généré avec Chrome ! Taille: {size_kb:.2f} KB")
                return True
            else:
                print("❌ Échec génération PDF - Vérifiez les logs Railway")
                return False
        else:
            print("❌ JSReport non accessible")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de test Chrome: {e}")
        return False

def show_deployment_instructions():
    """Affiche les instructions de déploiement Chrome"""
    print("\n📋 INSTRUCTIONS DÉPLOIEMENT CHROME")
    print("=" * 40)
    print("1. Dans votre repository JSReport:")
    print("   • Remplacez 'Dockerfile' par le contenu de 'Dockerfile.jsreport.chrome'")
    print("   • Remplacez 'jsreport.config.json' par 'jsreport.config.chrome.json'")
    print()
    print("2. Commitez et pushez:")
    print("   git add Dockerfile jsreport.config.json")
    print("   git commit -m 'Add Chrome for PDF generation'")
    print("   git push")
    print()
    print("3. Railway redéploie automatiquement (5-10 minutes)")
    print()
    print("4. Testez la génération PDF depuis Django")
    print()
    print("🎯 Résultat: Plus d'erreur Chrome, PDF générés ! 🎉")

if __name__ == "__main__":
    print("🚀 TEST CONFIGURATION CHROME JSREPORT")
    print("=" * 50)
    
    dockerfile_ok = test_chrome_config_files()
    config_ok = test_chrome_config_json()
    
    if dockerfile_ok and config_ok:
        print("\n🎉 CONFIGURATION CHROME PARFAITE !")
        print("Vous pouvez déployer sur Railway.")
        
        # Test de connexion si possible
        connection_result = test_jsreport_connection_chrome()
        
        if connection_result is True:
            print("\n🎉 CHROME FONCTIONNE PARFAITEMENT !")
            print("L'impression des factures est opérationnelle ! 🚀")
        elif connection_result is False:
            print("\n⚠️ PROBLÈME CHROME DÉTECTÉ")
            print("Vérifiez les logs Railway pour plus de détails.")
        else:
            print("\n📋 PRÊT POUR LE DÉPLOIEMENT")
            show_deployment_instructions()
    else:
        print("\n⚠️ CONFIGURATION À CORRIGER")
        print("Vérifiez les éléments marqués ❌ ci-dessus.")
        show_deployment_instructions()
    
    print("\n📚 Documentation:")
    print("   • CORRECTION_CHROME_JSREPORT.md")