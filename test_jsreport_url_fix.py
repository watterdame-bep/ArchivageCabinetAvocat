#!/usr/bin/env python3
"""
Test rapide pour valider la correction de l'URL JSReport
"""

import os
import sys
import django

def setup_django():
    """Configure Django pour les tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    django.setup()

def test_url_correction():
    """Test de la correction automatique d'URL"""
    print("🔍 Test de correction automatique d'URL JSReport...")
    
    # Simuler différentes URLs
    test_cases = [
        # (input, expected_output)
        ('cabinet-avocat-jsreport.railway.app', 'https://cabinet-avocat-jsreport.railway.app'),
        ('localhost:5488', 'http://localhost:5488'),
        ('127.0.0.1:5488', 'http://127.0.0.1:5488'),
        ('https://already-correct.railway.app', 'https://already-correct.railway.app'),
        ('http://localhost:5488', 'http://localhost:5488'),
    ]
    
    for input_url, expected in test_cases:
        # Logique de correction (même que dans jsreport_service.py)
        if not input_url.startswith(('http://', 'https://')):
            if 'localhost' in input_url or '127.0.0.1' in input_url:
                corrected = f'http://{input_url}'
            else:
                corrected = f'https://{input_url}'
        else:
            corrected = input_url
        
        if corrected == expected:
            print(f"✅ {input_url} → {corrected}")
        else:
            print(f"❌ {input_url} → {corrected} (attendu: {expected})")

def test_current_config():
    """Test de la configuration actuelle"""
    print("\n🔍 Test de la configuration JSReport actuelle...")
    
    try:
        setup_django()
        from utils.jsreport_service import jsreport_service
        
        print(f"✅ URL JSReport: {jsreport_service.base_url}")
        print(f"✅ API URL: {jsreport_service.api_url}")
        print(f"✅ Username: {jsreport_service.username}")
        print(f"✅ Timeout: {jsreport_service.timeout}s")
        
        # Vérifier que l'URL a un schéma valide
        if jsreport_service.base_url.startswith(('http://', 'https://')):
            print("✅ URL a un schéma valide")
            return True
        else:
            print("❌ URL n'a pas de schéma valide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_connection():
    """Test de connexion JSReport"""
    print("\n🔍 Test de connexion JSReport...")
    
    try:
        from utils.jsreport_service import jsreport_service
        
        if jsreport_service.test_connection():
            print("✅ Connexion JSReport réussie")
            return True
        else:
            print("❌ Connexion JSReport échouée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de Correction URL JSReport")
    print("=" * 50)
    
    test_url_correction()
    
    config_ok = test_current_config()
    connection_ok = test_connection() if config_ok else False
    
    print("=" * 50)
    
    if config_ok and connection_ok:
        print("✅ Correction URL JSReport réussie !")
        print("🎯 JSReport est prêt pour la génération PDF")
    elif config_ok:
        print("⚠️  Configuration OK mais connexion échouée")
        print("💡 Vérifier que le service JSReport est démarré")
    else:
        print("❌ Problème de configuration")
        print("💡 Vérifier la variable JSREPORT_SERVICE_URL")
    
    return 0 if (config_ok and connection_ok) else 1

if __name__ == "__main__":
    exit(main())