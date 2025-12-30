#!/usr/bin/env python3
"""
Script de test pour vérifier les URLs statiques
"""

import os
import sys
import django
from django.test import Client
from django.urls import reverse

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.conf import settings

def test_static_urls():
    """Teste les URLs statiques"""
    print("🌐 Test des URLs statiques\n")
    
    client = Client()
    
    # URLs à tester
    test_urls = [
        '/static/css/style.css',
        '/static/css/vendors_css.css',
        '/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        '/static/js/vendors.min.js',
        '/static/images/favicon.ico',
    ]
    
    print("📋 Test des URLs:")
    for url in test_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {url} - OK ({response.status_code})")
            elif response.status_code == 404:
                print(f"  ❌ {url} - NOT FOUND ({response.status_code})")
            else:
                print(f"  ⚠️  {url} - {response.status_code}")
        except Exception as e:
            print(f"  ❌ {url} - ERREUR: {e}")
    
    print(f"\n📊 Configuration:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    
    # Vérifier que les fichiers existent physiquement
    print(f"\n📁 Vérification physique:")
    from pathlib import Path
    static_root = Path(settings.STATIC_ROOT)
    
    if static_root.exists():
        css_files = list(static_root.glob('**/*.css'))
        print(f"  📊 Fichiers CSS trouvés: {len(css_files)}")
        
        # Vérifier bootstrap spécifiquement
        bootstrap_css = static_root / 'assets' / 'vendor_components' / 'bootstrap' / 'dist' / 'css' / 'bootstrap.css'
        if bootstrap_css.exists():
            print(f"  ✅ Bootstrap CSS: {bootstrap_css}")
        else:
            print(f"  ❌ Bootstrap CSS manquant: {bootstrap_css}")
    else:
        print(f"  ❌ STATIC_ROOT n'existe pas: {static_root}")

def main():
    """Fonction principale"""
    try:
        test_static_urls()
        print("\n✅ Test terminé")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()