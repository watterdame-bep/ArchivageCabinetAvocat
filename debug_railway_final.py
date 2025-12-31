#!/usr/bin/env python3
"""
Diagnostic final pour identifier pourquoi Railway a encore des 404
"""

import os
import sys
from pathlib import Path

def test_railway_environment():
    """Teste l'environnement Railway"""
    print("🔍 Test de l'environnement Railway\n")
    
    # Variables d'environnement Railway
    railway_vars = [
        'RAILWAY_ENVIRONMENT',
        'RAILWAY_PROJECT_ID', 
        'RAILWAY_SERVICE_ID',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    print("📋 Variables d'environnement Railway:")
    for var in railway_vars:
        value = os.environ.get(var, 'NON DÉFINIE')
        print(f"  {var}: {value}")
    
    # Vérifier si on est sur Railway
    is_railway = 'RAILWAY_ENVIRONMENT' in os.environ
    print(f"\n🚂 Environnement Railway détecté: {is_railway}")
    
    return is_railway

def test_django_settings():
    """Teste quelle configuration Django est chargée"""
    print("\n🔧 Test de la configuration Django\n")
    
    try:
        # Forcer settings_production si pas défini
        if 'DJANGO_SETTINGS_MODULE' not in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
            print("⚠️ DJANGO_SETTINGS_MODULE forcé à settings_production")
        
        import django
        django.setup()
        from django.conf import settings
        
        print(f"📋 Configuration Django chargée:")
        print(f"  Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  STATIC_URL: {settings.STATIC_URL}")
        print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Vérifier WhiteNoise
        whitenoise_found = any('whitenoise' in mw.lower() for mw in settings.MIDDLEWARE)
        print(f"  WhiteNoise middleware: {whitenoise_found}")
        print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        return settings
        
    except Exception as e:
        print(f"❌ Erreur chargement Django: {e}")
        return None

def test_static_files_existence():
    """Teste l'existence des fichiers statiques"""
    print("\n📁 Test de l'existence des fichiers statiques\n")
    
    # Fichiers qui causent des 404 selon les logs
    problematic_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'css/vendors_css.css',
        'css/style.css'
    ]
    
    # Tester dans static/ (source)
    print("📋 Fichiers dans static/ (source):")
    static_dir = Path('static')
    for file_path in problematic_files:
        full_path = static_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} MANQUANT")
    
    # Tester dans staticfiles/ (destination)
    print(f"\n📋 Fichiers dans staticfiles/ (destination):")
    staticfiles_dir = Path('staticfiles')
    if not staticfiles_dir.exists():
        print("  ❌ Dossier staticfiles n'existe pas")
        return False
    
    for file_path in problematic_files:
        full_path = staticfiles_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} MANQUANT dans staticfiles")
    
    return True

def test_collectstatic_simulation():
    """Simule collectstatic pour voir ce qui se passe"""
    print("\n🔄 Simulation de collectstatic\n")
    
    try:
        # Forcer settings_production
        os.environ['DJANGO_SETTINGS_MODULE'] = 'CabinetAvocat.settings_production'
        
        import django
        from django.core.management import execute_from_command_line
        
        django.setup()
        
        print("🚀 Exécution de collectstatic --dry-run...")
        
        # Dry run pour voir ce qui serait copié
        execute_from_command_line([
            'manage.py', 
            'collectstatic', 
            '--dry-run',
            '--noinput',
            '--verbosity=2'
        ])
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur collectstatic: {e}")
        return False

def create_railway_debug_endpoint():
    """Crée un endpoint de debug pour Railway"""
    debug_view = '''
# Ajouter dans urls.py pour debug Railway
from django.http import JsonResponse
from django.conf import settings
import os

def railway_debug(request):
    """Debug endpoint pour Railway"""
    return JsonResponse({
        'environment': {
            'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT'),
            'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE'),
        },
        'django_settings': {
            'DEBUG': settings.DEBUG,
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': str(settings.STATIC_ROOT),
            'STATICFILES_DIRS': [str(d) for d in settings.STATICFILES_DIRS],
            'STATICFILES_STORAGE': settings.STATICFILES_STORAGE,
        },
        'middleware': settings.MIDDLEWARE,
        'files_test': {
            'staticfiles_exists': os.path.exists(settings.STATIC_ROOT),
            'static_dir_exists': os.path.exists('static'),
        }
    })

# URL: path('railway-debug/', railway_debug, name='railway_debug'),
'''
    
    with open('railway_debug_endpoint.py', 'w', encoding='utf-8') as f:
        f.write(debug_view)
    
    print("📝 Endpoint de debug créé dans railway_debug_endpoint.py")

def main():
    """Fonction principale"""
    print("🚀 Diagnostic Final Railway - Pourquoi les 404 persistent ?\n")
    
    try:
        # Tests séquentiels
        is_railway = test_railway_environment()
        settings = test_django_settings()
        files_exist = test_static_files_existence()
        
        print("\n" + "="*60)
        print("📋 DIAGNOSTIC FINAL")
        print("="*60)
        
        if not settings:
            print("\n🚨 PROBLÈME CRITIQUE: Django ne se charge pas")
            print("  - Vérifier DJANGO_SETTINGS_MODULE")
            print("  - Vérifier les imports dans settings_production.py")
        
        elif settings.STATICFILES_DIRS == []:
            print("\n🚨 PROBLÈME CRITIQUE: STATICFILES_DIRS vide")
            print("  - Railway n'utilise pas settings_production.py")
            print("  - start_railway.py ne force pas correctement les settings")
        
        elif not files_exist:
            print("\n🚨 PROBLÈME CRITIQUE: Fichiers statiques manquants")
            print("  - collectstatic ne s'exécute pas correctement")
            print("  - Dossier staticfiles non créé")
        
        else:
            print("\n🤔 PROBLÈME MYSTÉRIEUX:")
            print("  - Configuration semble correcte")
            print("  - Fichiers semblent exister")
            print("  - Mais Railway retourne toujours 404")
            print("\n💡 Solutions à essayer:")
            print("  1. Vérifier l'endpoint /railway-debug/ sur Railway")
            print("  2. Tester les URLs directes des fichiers CSS")
            print("  3. Vérifier les logs de collectstatic sur Railway")
        
        create_railway_debug_endpoint()
        
        print(f"\n🔧 Prochaines étapes:")
        print(f"  1. Ajouter l'endpoint de debug aux URLs")
        print(f"  2. Déployer et tester /railway-debug/")
        print(f"  3. Analyser la réponse pour identifier le problème exact")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()