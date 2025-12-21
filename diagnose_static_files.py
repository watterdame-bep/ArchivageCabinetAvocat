#!/usr/bin/env python
"""
Script de diagnostic pour les fichiers statiques Django
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.test import Client

def diagnose_static_files():
    """Diagnostic complet des fichiers statiques"""
    
    print("🔍 DIAGNOSTIC DES FICHIERS STATIQUES")
    print("=" * 50)
    
    # 1. Configuration Django
    print("\n📋 CONFIGURATION DJANGO:")
    print(f"DEBUG = {settings.DEBUG}")
    print(f"STATIC_URL = {settings.STATIC_URL}")
    print(f"STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
    print(f"STATIC_ROOT = {settings.STATIC_ROOT}")
    
    # 2. Vérification des dossiers
    print("\n📁 VÉRIFICATION DES DOSSIERS:")
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"✅ {static_dir} existe")
            # Lister quelques fichiers
            css_dir = static_dir / "css"
            js_dir = static_dir / "js"
            if css_dir.exists():
                css_files = list(css_dir.glob("*.css"))[:3]
                print(f"   📄 CSS trouvés: {[f.name for f in css_files]}")
            if js_dir.exists():
                js_files = list(js_dir.glob("*.js"))[:3]
                print(f"   📄 JS trouvés: {[f.name for f in js_files]}")
        else:
            print(f"❌ {static_dir} n'existe pas")
    
    # 3. Test de recherche de fichiers critiques
    print("\n🔍 TEST DE RECHERCHE DE FICHIERS:")
    critical_files = [
        'css/style.css',
        'css/vendors_css.css',
        'js/vendors.min.js',
        'images/favicon.ico'
    ]
    
    for file_path in critical_files:
        found = find(file_path)
        if found:
            print(f"✅ {file_path} trouvé: {found}")
        else:
            print(f"❌ {file_path} NON TROUVÉ")
    
    # 4. Test d'accès HTTP
    print("\n🌐 TEST D'ACCÈS HTTP:")
    client = Client()
    
    test_urls = [
        '/static/',
        '/static/css/style.css',
        '/static/js/vendors.min.js'
    ]
    
    for url in test_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {url} accessible (200)")
            elif response.status_code == 404:
                print(f"❌ {url} non trouvé (404)")
            else:
                print(f"⚠️ {url} status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} erreur: {e}")
    
    # 5. Recommandations
    print("\n💡 RECOMMANDATIONS:")
    
    if settings.DEBUG:
        print("✅ Mode DEBUG activé - bon pour le développement")
    else:
        print("⚠️ Mode DEBUG désactivé - collectstatic requis")
    
    # Vérifier si collectstatic a été exécuté
    if settings.STATIC_ROOT and os.path.exists(settings.STATIC_ROOT):
        static_root_files = list(Path(settings.STATIC_ROOT).rglob("*"))
        if static_root_files:
            print(f"✅ STATIC_ROOT contient {len(static_root_files)} fichiers")
        else:
            print("⚠️ STATIC_ROOT existe mais est vide")
    else:
        print("⚠️ STATIC_ROOT n'existe pas ou n'est pas défini")
    
    print("\n🎯 SOLUTIONS RECOMMANDÉES:")
    print("1. Vérifier que les templates utilisent {% load static %}")
    print("2. Utiliser {% static 'path/file.ext' %} dans les templates")
    print("3. Si problème persiste: python manage.py collectstatic")
    print("4. Puis: python manage.py runserver --insecure")
    
    return True

if __name__ == '__main__':
    diagnose_static_files()