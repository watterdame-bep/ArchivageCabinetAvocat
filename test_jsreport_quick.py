#!/usr/bin/env python
"""
Test rapide JSReport - Vérification configuration Railway
"""
import os
import sys
import django
import requests

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings

def test_jsreport_config():
    """Test rapide de la configuration JSReport"""
    print("🔧 CONFIGURATION JSREPORT ACTUELLE")
    print("=" * 40)
    
    jsreport_url = getattr(settings, 'JSREPORT_URL', 'NON DÉFINI')
    username = getattr(settings, 'JSREPORT_USERNAME', 'NON DÉFINI')
    password = getattr(settings, 'JSREPORT_PASSWORD', 'NON DÉFINI')
    
    print(f"URL: {jsreport_url}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password != 'NON DÉFINI' else 'NON DÉFINI'}")
    print()
    
    # Vérification critique
    if jsreport_url == 'http://localhost:5488':
        print("❌ PROBLÈME IDENTIFIÉ!")
        print("   JSREPORT_URL pointe vers localhost")
        print("   En production Railway, cela ne fonctionnera pas")
        print()
        print("💡 SOLUTION:")
        print("   1. Déployez JSReport comme service séparé sur Railway")
        print("   2. Configurez JSREPORT_URL avec l'URL Railway de JSReport")
        print("   Exemple: https://votre-jsreport-service.railway.app")
        return False
    elif 'localhost' in jsreport_url:
        print("❌ PROBLÈME: URL contient 'localhost'")
        return False
    elif jsreport_url.startswith('https://'):
        print("✅ URL semble correcte pour la production")
        return True
    else:
        print("⚠️ URL suspecte, vérifiez qu'elle est correcte")
        return False

def test_connection_quick():
    """Test de connexion rapide"""
    print("🔗 TEST DE CONNEXION RAPIDE")
    print("=" * 40)
    
    jsreport_url = getattr(settings, 'JSREPORT_URL', '')
    
    if not jsreport_url or 'localhost' in jsreport_url:
        print("❌ Impossible de tester - URL localhost ou manquante")
        return False
        
    try:
        ping_url = f"{jsreport_url}/api/ping"
        print(f"Test: {ping_url}")
        
        response = requests.get(ping_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ JSReport accessible")
            return True
        else:
            print(f"❌ JSReport non accessible (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion")
        print("💡 Service JSReport probablement non déployé ou arrêté")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TEST RAPIDE JSREPORT")
    print("=" * 50)
    
    config_ok = test_jsreport_config()
    
    if config_ok:
        connection_ok = test_connection_quick()
        
        if connection_ok:
            print("\n✅ Configuration semble correcte")
            print("💡 Si l'impression ne fonctionne toujours pas:")
            print("   - Vérifiez les templates dans JSReport")
            print("   - Consultez les logs Railway")
        else:
            print("\n❌ Problème de connexion au service JSReport")
    else:
        print("\n❌ Problème de configuration détecté")
        
    print("\n📋 Pour un diagnostic complet:")
    print("   python diagnostic_jsreport_railway.py")