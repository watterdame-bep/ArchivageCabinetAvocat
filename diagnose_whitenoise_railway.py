#!/usr/bin/env python3
"""
Script de diagnostic avancé pour WhiteNoise sur Railway
"""

import os
import sys
from pathlib import Path

def check_whitenoise_configuration():
    """Vérifie la configuration WhiteNoise en détail"""
    print("🔍 Diagnostic WhiteNoise Railway\n")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    import django
    django.setup()
    from django.conf import settings
    
    print("📋 Configuration actuelle:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print(f"  DEBUG: {settings.DEBUG}")
    
    # Vérifier le middleware
    print(f"\n🔧 Middleware:")
    for i, middleware in enumerate(settings.MIDDLEWARE):
        marker = "👉" if "whitenoise" in middleware.lower() else "  "
        print(f"  {i+1:2d}. {marker} {middleware}")
    
    return settings

def check_static_files_structure():
    """Vérifie la structure des fichiers statiques"""
    print("\n📁 Structure des fichiers statiques:")
    
    staticfiles_dir = Path('staticfiles')
    if not staticfiles_dir.exists():
        print("  ❌ Dossier staticfiles n'existe pas")
        return False
    
    # Compter les fichiers
    total_files = sum(1 for _ in staticfiles_dir.rglob('*') if _.is_file())
    print(f"  📊 Total: {total_files} fichiers")
    
    # Vérifier les dossiers critiques
    critical_dirs = [
        'css',
        'assets/vendor_components/bootstrap/dist/css',
        'assets/vendor_components/select2/dist/css',
        'assets/vendor_components/OwlCarousel2/dist/assets'
    ]
    
    for dir_path in critical_dirs:
        full_path = staticfiles_dir / dir_path
        if full_path.exists():
            file_count = sum(1 for _ in full_path.rglob('*') if _.is_file())
            print(f"  ✅ {dir_path}: {file_count} fichiers")
        else:
            print(f"  ❌ {dir_path}: MANQUANT")
    
    return True

def test_direct_file_access():
    """Teste l'accès direct aux fichiers problématiques"""
    print("\n🧪 Test d'accès direct aux fichiers:")
    
    staticfiles_dir = Path('staticfiles')
    problematic_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'css/vendors_css.css'
    ]
    
    for file_path in problematic_files:
        full_path = staticfiles_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} MANQUANT")

def analyze_whitenoise_issue():
    """Analyse les problèmes potentiels avec WhiteNoise"""
    print("\n🔍 Analyse des problèmes WhiteNoise:")
    
    # Problème 1: STATICFILES_DIRS en production
    print("\n1. STATICFILES_DIRS en production:")
    print("   ⚠️ STATICFILES_DIRS peut causer des conflits avec WhiteNoise")
    print("   💡 Solution: Vider STATICFILES_DIRS en production")
    
    # Problème 2: Ordre du middleware
    print("\n2. Ordre du middleware:")
    print("   ⚠️ WhiteNoise doit être après SecurityMiddleware")
    print("   💡 Solution: Vérifier l'ordre dans MIDDLEWARE")
    
    # Problème 3: STATICFILES_STORAGE
    print("\n3. STATICFILES_STORAGE:")
    print("   ⚠️ CompressedStaticFilesStorage peut avoir des problèmes")
    print("   💡 Solution: Essayer StaticFilesStorage temporairement")
    
    # Problème 4: URLs serving
    print("\n4. URLs serving:")
    print("   ⚠️ urls.py peut interférer avec WhiteNoise")
    print("   💡 Solution: Supprimer static() en production")

def create_whitenoise_fix():
    """Crée une configuration WhiteNoise corrigée"""
    print("\n🔧 Création d'une configuration WhiteNoise corrigée...")
    
    fix_content = '''
# Configuration WhiteNoise ULTRA-SIMPLE pour Railway
# À ajouter dans settings_production.py

# 1. Vider STATICFILES_DIRS en production (CRITIQUE)
STATICFILES_DIRS = []

# 2. Configuration WhiteNoise simple
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# 3. Middleware WhiteNoise (vérifier l'ordre)
# MIDDLEWARE doit contenir:
# 'django.middleware.security.SecurityMiddleware',
# 'whitenoise.middleware.WhiteNoiseMiddleware',  # JUSTE APRÈS Security

# 4. Configuration WhiteNoise permissive
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['css', 'js']  # Pas de compression CSS/JS
WHITENOISE_MAX_AGE = 0  # Pas de cache

# 5. Supprimer les URLs statiques de urls.py en production
# Commenter ces lignes dans urls.py:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
    
    with open('whitenoise_fix_config.txt', 'w', encoding='utf-8') as f:
        f.write(fix_content)
    
    print("✅ Configuration créée dans whitenoise_fix_config.txt")

def main():
    """Fonction principale"""
    print("🚀 Diagnostic WhiteNoise Railway\n")
    
    try:
        settings = check_whitenoise_configuration()
        check_static_files_structure()
        test_direct_file_access()
        analyze_whitenoise_issue()
        create_whitenoise_fix()
        
        print("\n" + "="*60)
        print("📋 RÉSUMÉ DU DIAGNOSTIC")
        print("="*60)
        
        print("\n🚨 PROBLÈME IDENTIFIÉ:")
        print("  Les fichiers existent mais WhiteNoise ne les sert pas")
        
        print("\n💡 SOLUTIONS À ESSAYER:")
        print("  1. Vider STATICFILES_DIRS = [] en production")
        print("  2. Utiliser StaticFilesStorage au lieu de CompressedStaticFilesStorage")
        print("  3. Supprimer static() URLs de urls.py")
        print("  4. Vérifier l'ordre du middleware WhiteNoise")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. Appliquer les corrections suggérées")
        print("  2. Redéployer sur Railway")
        print("  3. Tester les URLs directes")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()