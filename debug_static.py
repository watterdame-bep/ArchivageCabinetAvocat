#!/usr/bin/env python
"""
Debug des fichiers statiques pour Railway
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')

django.setup()

from django.conf import settings
from django.contrib.staticfiles import finders

def check_static_config():
    """Vérifier la configuration des fichiers statiques"""
    print("🔍 Configuration des fichiers statiques:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")

def check_critical_files():
    """Vérifier les fichiers CSS critiques"""
    print("\n🎨 Vérification des fichiers CSS critiques:")
    
    critical_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'css/style.css',
        'css/vendors_css.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
    ]
    
    for file_path in critical_files:
        # Chercher avec Django finders
        found_path = finders.find(file_path)
        if found_path:
            print(f"  ✅ {file_path} -> {found_path}")
        else:
            print(f"  ❌ {file_path} -> NON TROUVÉ")
            
        # Vérifier dans staticfiles après collecte
        static_file = os.path.join(settings.STATIC_ROOT, file_path)
        if os.path.exists(static_file):
            print(f"     ✅ Présent dans staticfiles")
        else:
            print(f"     ❌ Absent de staticfiles")

def check_staticfiles_directory():
    """Vérifier le contenu du répertoire staticfiles"""
    print(f"\n📁 Contenu de {settings.STATIC_ROOT}:")
    
    if os.path.exists(settings.STATIC_ROOT):
        # Lister les premiers niveaux
        for item in sorted(os.listdir(settings.STATIC_ROOT))[:10]:
            item_path = os.path.join(settings.STATIC_ROOT, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
        
        # Vérifier spécifiquement Bootstrap
        bootstrap_path = os.path.join(settings.STATIC_ROOT, 'assets', 'vendor_components', 'bootstrap')
        if os.path.exists(bootstrap_path):
            print(f"\n✅ Dossier Bootstrap trouvé: {bootstrap_path}")
            css_path = os.path.join(bootstrap_path, 'dist', 'css')
            if os.path.exists(css_path):
                print(f"✅ Dossier CSS Bootstrap: {css_path}")
                css_files = os.listdir(css_path)
                print(f"   Fichiers CSS: {css_files}")
            else:
                print(f"❌ Dossier CSS Bootstrap manquant")
        else:
            print(f"❌ Dossier Bootstrap manquant")
    else:
        print(f"❌ Répertoire staticfiles n'existe pas")

def main():
    print("🔍 Debug des fichiers statiques Railway")
    print("=" * 50)
    
    check_static_config()
    check_critical_files()
    check_staticfiles_directory()

if __name__ == '__main__':
    main()