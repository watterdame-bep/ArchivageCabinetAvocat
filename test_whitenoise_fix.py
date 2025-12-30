#!/usr/bin/env python3
"""
Script de test pour vérifier la correction WhiteNoise sur Railway
"""

import os
import sys
from pathlib import Path

def test_whitenoise_configuration():
    """Teste la nouvelle configuration WhiteNoise"""
    print("🧪 Test de la configuration WhiteNoise corrigée\n")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    import django
    django.setup()
    from django.conf import settings
    
    print("✅ Configuration WhiteNoise:")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Vérifications critiques
    checks = []
    
    # 1. STATICFILES_DIRS doit être vide
    if not settings.STATICFILES_DIRS:
        checks.append("✅ STATICFILES_DIRS est vide (correct)")
    else:
        checks.append("❌ STATICFILES_DIRS n'est pas vide (problème)")
    
    # 2. WhiteNoise middleware présent
    whitenoise_found = any('whitenoise' in mw.lower() for mw in settings.MIDDLEWARE)
    if whitenoise_found:
        checks.append("✅ WhiteNoise middleware présent")
    else:
        checks.append("❌ WhiteNoise middleware manquant")
    
    # 3. Ordre du middleware
    security_idx = -1
    whitenoise_idx = -1
    for i, mw in enumerate(settings.MIDDLEWARE):
        if 'SecurityMiddleware' in mw:
            security_idx = i
        if 'whitenoise' in mw.lower():
            whitenoise_idx = i
    
    if security_idx >= 0 and whitenoise_idx >= 0 and whitenoise_idx == security_idx + 1:
        checks.append("✅ WhiteNoise après SecurityMiddleware (correct)")
    else:
        checks.append("❌ Ordre du middleware incorrect")
    
    print(f"\n📋 Vérifications:")
    for check in checks:
        print(f"  {check}")
    
    return all("✅" in check for check in checks)

def test_static_files_exist():
    """Vérifie que les fichiers statiques existent"""
    print("\n📁 Vérification des fichiers statiques:")
    
    staticfiles_dir = Path('staticfiles')
    if not staticfiles_dir.exists():
        print("  ❌ Dossier staticfiles n'existe pas - exécuter collectstatic")
        return False
    
    # Fichiers critiques qui causaient des 404
    critical_files = [
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'assets/vendor_components/select2/dist/css/select2.min.css',
        'assets/vendor_components/OwlCarousel2/dist/assets/owl.carousel.css',
        'css/vendors_css.css',
        'css/style.css'
    ]
    
    all_exist = True
    for file_path in critical_files:
        full_path = staticfiles_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_path} MANQUANT")
            all_exist = False
    
    return all_exist

def create_deployment_instructions():
    """Crée les instructions de déploiement"""
    instructions = """
🚀 INSTRUCTIONS DE DÉPLOIEMENT RAILWAY

1. 📋 Vérifications avant déploiement:
   ✅ STATICFILES_DIRS = [] (vide)
   ✅ WhiteNoise middleware après SecurityMiddleware
   ✅ Pas de static() URLs en production
   ✅ Fichiers statiques présents dans staticfiles/

2. 🔧 Commandes de déploiement:
   git add .
   git commit -m "Fix: WhiteNoise configuration for Railway static files"
   git push origin main

3. 🧪 Tests après déploiement:
   - Ouvrir: https://ton-app.up.railway.app/
   - Tester: https://ton-app.up.railway.app/static/assets/vendor_components/bootstrap/dist/css/bootstrap.css
   - Vérifier: Design CSS complet

4. 🔍 Si problème persiste:
   - Vérifier les logs Railway
   - Tester l'endpoint: /test-static/
   - Vérifier que collectstatic s'exécute

💡 POINTS CLÉS:
- WhiteNoise gère TOUS les fichiers statiques en production
- Django ne doit PAS servir les static files quand DEBUG=False
- STATICFILES_DIRS vide évite les conflits avec collectstatic
"""
    
    with open('WHITENOISE_DEPLOYMENT.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("📝 Instructions créées dans WHITENOISE_DEPLOYMENT.md")

def main():
    """Fonction principale"""
    print("🚀 Test de la correction WhiteNoise\n")
    
    try:
        config_ok = test_whitenoise_configuration()
        files_ok = test_static_files_exist()
        
        print("\n" + "="*50)
        print("📋 RÉSULTAT DU TEST")
        print("="*50)
        
        if config_ok and files_ok:
            print("✅ CONFIGURATION CORRECTE")
            print("🚀 Prêt pour le déploiement Railway")
            create_deployment_instructions()
        else:
            print("❌ PROBLÈMES DÉTECTÉS")
            if not config_ok:
                print("  - Configuration WhiteNoise incorrecte")
            if not files_ok:
                print("  - Fichiers statiques manquants")
        
        print(f"\n🔧 Prochaines étapes:")
        print(f"  1. Corriger les problèmes identifiés")
        print(f"  2. Exécuter: python manage.py collectstatic --noinput")
        print(f"  3. Déployer sur Railway")
        print(f"  4. Tester les URLs statiques")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()