#!/usr/bin/env python3
"""
Script de diagnostic pour les erreurs 404 des fichiers statiques
"""

import os
import sys
from pathlib import Path

def diagnose_static_files():
    """Diagnostique les problèmes de fichiers statiques"""
    print("🔍 Diagnostic des erreurs 404 fichiers statiques\n")
    
    # Fichiers recherchés dans les logs d'erreur
    missing_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.theme.default.min.css',
        'assets/vendor_components/Magnific-Popup-master/dist/magnific-popup.css',
        'assets/vendor_components/lightbox-master/dist/ekko-lightbox.css',
        'assets/vendor_components/x-editable/dist/bootstrap3-editable/css/bootstrap-editable.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/bootstrap-datepicker/dist/css/bootstrap-datepicker.min.css',
        'assets/vendor_components/bootstrap-colorpicker/dist/css/bootstrap-colorpicker.min.css',
        'assets/vendor_components/bootstrap-select/dist/css/bootstrap-select.css',
        'assets/vendor_components/bootstrap-tagsinput/dist/bootstrap-tagsinput.css',
        'assets/vendor_components/bootstrap-touchspin/dist/jquery.bootstrap-touchspin.css',
        'assets/vendor_components/raty-master/lib/jquery.raty.css',
    ]
    
    print("📁 Vérification dans static/ (source):")
    static_dir = Path('static')
    for file_path in missing_files:
        full_path = static_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MANQUANT DANS SOURCE")
    
    print("\n📁 Vérification dans staticfiles/ (collecté):")
    staticfiles_dir = Path('staticfiles')
    for file_path in missing_files:
        full_path = staticfiles_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MANQUANT DANS COLLECTÉ")
    
    print("\n🔍 Analyse du problème:")
    
    # Vérifier vendors_css.css
    vendors_css_static = Path('static/css/vendors_css.css')
    vendors_css_collected = Path('staticfiles/css/vendors_css.css')
    
    if vendors_css_static.exists() and vendors_css_collected.exists():
        with open(vendors_css_static, 'r', encoding='utf-8') as f:
            static_content = f.read()
        with open(vendors_css_collected, 'r', encoding='utf-8') as f:
            collected_content = f.read()
        
        if '../assets/' in static_content and '../assets/' in collected_content:
            print("  ✅ vendors_css.css utilise des URLs relatives")
        else:
            print("  ❌ vendors_css.css utilise encore des URLs absolues")
            
        # Compter les @import
        static_imports = static_content.count('@import')
        collected_imports = collected_content.count('@import')
        print(f"  📊 Imports dans static/: {static_imports}")
        print(f"  📊 Imports dans staticfiles/: {collected_imports}")
    
    print("\n💡 Solutions possibles:")
    
    # Vérifier si le problème vient des templates
    print("  🔧 Vérifier que les templates utilisent {% static %}")
    print("  🔧 Vérifier que urls.py sert les fichiers statiques en production")
    print("  🔧 Vérifier que Railway exécute collectstatic au build")
    print("  🔧 Forcer un redéploiement complet sur Railway")
    
    # Vérifier la configuration
    print("\n🔍 Configuration actuelle:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        import django
        django.setup()
        from django.conf import settings
        
        print(f"  STATIC_URL: {settings.STATIC_URL}")
        print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Vérifier les URLs
        from django.urls import get_resolver
        resolver = get_resolver()
        print("  ✅ URLs Django configurées")
        
    except Exception as e:
        print(f"  ❌ Erreur configuration: {e}")
    
    print("\n🚀 Actions recommandées:")
    print("  1. Vérifier que Railway exécute 'collectstatic' au build")
    print("  2. Forcer un redéploiement complet")
    print("  3. Tester une URL directe: https://votre-app.up.railway.app/static/css/style.css")
    print("  4. Vérifier les logs Railway pour les erreurs de build")

def main():
    """Fonction principale"""
    try:
        diagnose_static_files()
        print("\n✅ Diagnostic terminé")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()