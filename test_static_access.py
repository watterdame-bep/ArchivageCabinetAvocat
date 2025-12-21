#!/usr/bin/env python
"""
Test d'accès aux fichiers statiques - Diagnostic précis
"""
import os
import sys
import django
import subprocess
import time
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.test import Client
from django.urls import reverse

def test_static_access():
    """Test complet d'accès aux fichiers statiques"""
    
    print("🔍 TEST D'ACCÈS AUX FICHIERS STATIQUES")
    print("=" * 50)
    
    # 1. Configuration actuelle
    print("\n📋 CONFIGURATION ACTUELLE:")
    print(f"DEBUG = {settings.DEBUG}")
    print(f"STATIC_URL = {settings.STATIC_URL}")
    print(f"STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
    print(f"STATIC_ROOT = {settings.STATIC_ROOT}")
    
    # 2. Test de recherche des fichiers critiques
    print("\n🔍 RECHERCHE DES FICHIERS CRITIQUES:")
    critical_files = [
        'css/style.css',
        'css/vendors_css.css', 
        'css/skin_color.css',
        'js/vendors.min.js',
        'js/template.js',
        'images/favicon.ico'
    ]
    
    found_files = []
    missing_files = []
    
    for file_path in critical_files:
        found = find(file_path)
        if found:
            print(f"✅ {file_path} → {found}")
            found_files.append(file_path)
        else:
            print(f"❌ {file_path} → NON TROUVÉ")
            missing_files.append(file_path)
    
    # 3. Test d'existence physique
    print("\n📁 VÉRIFICATION PHYSIQUE DES FICHIERS:")
    static_dir = Path("static")
    
    for file_path in critical_files:
        full_path = static_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} existe ({size} bytes)")
        else:
            print(f"❌ {file_path} n'existe pas physiquement")
    
    # 4. Test de la configuration URLs
    print("\n🌐 TEST DE LA CONFIGURATION URLS:")
    try:
        from CabinetAvocat.urls import urlpatterns
        static_configured = False
        
        # Chercher la configuration static dans urls.py
        urls_content = open('CabinetAvocat/urls.py', 'r', encoding='utf-8').read()
        if 'static(' in urls_content and 'STATICFILES_DIRS' in urls_content:
            print("✅ Configuration static trouvée dans urls.py avec STATICFILES_DIRS")
            static_configured = True
        elif 'static(' in urls_content and 'STATIC_ROOT' in urls_content:
            print("⚠️ Configuration static utilise STATIC_ROOT (peut causer des problèmes en DEBUG=True)")
        else:
            print("❌ Configuration static non trouvée dans urls.py")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des URLs: {e}")
    
    # 5. Recommandations basées sur les résultats
    print("\n💡 DIAGNOSTIC ET RECOMMANDATIONS:")
    
    if len(found_files) == len(critical_files):
        print("✅ Tous les fichiers critiques sont trouvés par Django")
    else:
        print(f"⚠️ {len(missing_files)} fichiers manquants sur {len(critical_files)}")
    
    if settings.DEBUG:
        print("✅ Mode DEBUG activé - bon pour le développement")
        print("👉 Django devrait servir les fichiers depuis STATICFILES_DIRS")
    else:
        print("⚠️ Mode DEBUG désactivé - collectstatic requis")
    
    # 6. Instructions de test manuel
    print("\n🧪 TESTS MANUELS À FAIRE:")
    print("1. Démarrez le serveur: python manage.py runserver")
    print("2. Ouvrez dans votre navigateur:")
    print("   - http://127.0.0.1:8000/static/")
    print("   - http://127.0.0.1:8000/static/css/style.css")
    print("   - http://127.0.0.1:8000/static/js/vendors.min.js")
    print("\n3. Résultats attendus:")
    print("   ✅ /static/ → Liste des dossiers (css, js, images, etc.)")
    print("   ✅ /static/css/style.css → Contenu du fichier CSS")
    print("   ✅ /static/js/vendors.min.js → Contenu du fichier JS")
    print("   ❌ Si vous voyez 404 → Problème de configuration")
    
    # 7. Test avec le template
    print("\n📄 VÉRIFICATION DU TEMPLATE:")
    template_path = Path("templates/admin_template/base.html")
    if template_path.exists():
        content = template_path.read_text(encoding='utf-8')
        if '{% load static %}' in content:
            print("✅ Template utilise {% load static %}")
        else:
            print("❌ Template n'utilise PAS {% load static %}")
            
        if '{% static ' in content:
            print("✅ Template utilise {% static 'path' %}")
        else:
            print("❌ Template n'utilise PAS {% static 'path' %}")
    
    # 8. Solution rapide si problème
    print("\n🚀 SOLUTION RAPIDE SI LE PROBLÈME PERSISTE:")
    print("1. Exécutez: python manage.py collectstatic --noinput")
    print("2. Puis: python manage.py runserver --insecure")
    print("3. Cela force Django à servir TOUS les fichiers statiques")
    
    return True

if __name__ == '__main__':
    test_static_access()