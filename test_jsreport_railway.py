#!/usr/bin/env python3
"""
Script pour tester JSReport avec les optimisations Railway
"""

import os
import sys
import django
import requests
import time
from pathlib import Path

def setup_django():
    """Configure Django pour les tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    django.setup()

def test_jsreport_connection():
    """Test de connexion JSReport"""
    print("🔍 Test de connexion JSReport...")
    
    from utils.jsreport_service import jsreport_service
    
    if jsreport_service.test_connection():
        print("✅ Connexion JSReport réussie")
        return True
    else:
        print("❌ Connexion JSReport échouée")
        return False

def test_jsreport_templates():
    """Test de récupération des templates"""
    print("\n🔍 Test des templates JSReport...")
    
    from utils.jsreport_service import jsreport_service
    
    templates = jsreport_service.get_templates()
    
    if templates:
        print(f"✅ {len(templates)} templates trouvés:")
        for template in templates[:5]:  # Afficher les 5 premiers
            print(f"  - {template.get('name', 'Sans nom')}")
        return True
    else:
        print("❌ Impossible de récupérer les templates")
        return False

def test_simple_pdf_generation():
    """Test de génération PDF simple"""
    print("\n🔍 Test de génération PDF simple...")
    
    from utils.jsreport_service import jsreport_service
    
    # Données de test simples
    test_data = {
        "title": "Test Railway",
        "date": "2025-12-31",
        "content": "Test de génération PDF sur Railway"
    }
    
    # Options optimisées pour Railway
    options = {
        "preview": False,
        "timeout": 180000,  # 3 minutes
    }
    
    print("⏳ Génération en cours (peut prendre jusqu'à 3 minutes)...")
    start_time = time.time()
    
    try:
        # Essayer avec un template simple (remplacer par un template existant)
        pdf_content = jsreport_service.generate_pdf(
            template_name="rapport_client",  # Remplacer par un template existant
            data=test_data,
            options=options
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if pdf_content:
            print(f"✅ PDF généré avec succès en {duration:.2f}s")
            print(f"📄 Taille: {len(pdf_content)} bytes")
            
            # Sauvegarder le PDF de test
            with open('test_railway.pdf', 'wb') as f:
                f.write(pdf_content)
            print("💾 PDF sauvegardé: test_railway.pdf")
            
            return True
        else:
            print(f"❌ Génération échouée après {duration:.2f}s")
            return False
            
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"💥 Erreur après {duration:.2f}s: {str(e)}")
        return False

def test_jsreport_config():
    """Test de la configuration JSReport"""
    print("\n🔍 Test de la configuration JSReport...")
    
    from django.conf import settings
    
    # Vérifier les variables de configuration
    config_vars = [
        ('JSREPORT_URL', getattr(settings, 'JSREPORT_URL', None)),
        ('JSREPORT_USERNAME', getattr(settings, 'JSREPORT_USERNAME', None)),
        ('JSREPORT_TIMEOUT', getattr(settings, 'JSREPORT_TIMEOUT', None)),
    ]
    
    for var_name, var_value in config_vars:
        if var_value:
            if 'PASSWORD' in var_name:
                print(f"✅ {var_name}: ***")
            else:
                print(f"✅ {var_name}: {var_value}")
        else:
            print(f"❌ {var_name}: Non configuré")
    
    # Vérifier la configuration JSREPORT_CONFIG
    if hasattr(settings, 'JSREPORT_CONFIG'):
        config = settings.JSREPORT_CONFIG
        print(f"✅ JSREPORT_CONFIG trouvé")
        print(f"  - URL: {config.get('url')}")
        print(f"  - Timeout: {config.get('timeout')}ms")
        print(f"  - Chrome timeout: {config.get('chrome_timeout')}ms")
        print(f"  - Preview: {config.get('preview')}")
        print(f"  - Templates: {len(config.get('templates', {}))}")
        return True
    else:
        print("❌ JSREPORT_CONFIG non trouvé")
        return False

def test_railway_variables():
    """Test des variables d'environnement Railway"""
    print("\n🔍 Test des variables d'environnement Railway...")
    
    railway_vars = [
        'JSREPORT_SERVICE_URL',
        'JSREPORT_USERNAME',
        'JSREPORT_PASSWORD',
        'JSREPORT_TIMEOUT',
        'RAILWAY_ENVIRONMENT'
    ]
    
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var:
                print(f"✅ {var}: ***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Non défini")

def main():
    """Fonction principale"""
    print("🚀 Test JSReport Railway - Optimisations Chrome Timeout")
    print("=" * 60)
    
    try:
        setup_django()
        
        tests = [
            test_railway_variables(),
            test_jsreport_config(),
            test_jsreport_connection(),
            test_jsreport_templates(),
            # test_simple_pdf_generation(),  # Décommenter pour tester la génération
        ]
        
        print("=" * 60)
        
        if all(tests):
            print("✅ Tous les tests passés !")
            print("\n📋 Prochaines étapes :")
            print("1. Configurer les variables JSReport sur Railway :")
            print("   JSREPORT_CHROME_TIMEOUT=180000")
            print("   JSREPORT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage")
            print("   JSREPORT_CHROME_POOL_SIZE=1")
            print("2. Redéployer JSReport service")
            print("3. Tester la génération PDF")
        else:
            print("❌ Certains tests ont échoué")
            return 1
        
    except Exception as e:
        print(f"💥 Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())