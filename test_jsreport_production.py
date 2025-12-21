#!/usr/bin/env python
import os
import sys
import django
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service

def test_production_jsreport():
    print("🧪 TEST JSREPORT PRODUCTION")
    print("=" * 40)
    
    url = settings.JSREPORT_URL
    print(f"URL: {url}")
    
    if 'localhost' in url:
        print("❌ URL contient encore localhost!")
        return False
        
    # Test de connexion
    if jsreport_service.test_connection():
        print("✅ Connexion OK")
        
        # Test des templates
        templates = jsreport_service.get_templates()
        if templates:
            print(f"✅ Templates: {len(templates)} trouvés")
            return True
        else:
            print("❌ Aucun template trouvé")
            return False
    else:
        print("❌ Connexion échouée")
        return False

if __name__ == "__main__":
    test_production_jsreport()
