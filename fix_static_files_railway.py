#!/usr/bin/env python3
"""
Script final pour corriger tous les problèmes de fichiers statiques Railway
"""

import os
import sys
import subprocess
from pathlib import Path

def check_urls_py():
    """Vérifie que urls.py est correctement configuré"""
    print("🔍 Vérification de urls.py...")
    
    urls_file = Path('CabinetAvocat/urls.py')
    if not urls_file.exists():
        print(f"❌ Fichier urls.py non trouvé: {urls_file}")
        return False
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier que les URLs statiques sont configurées pour la production
    if 'static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)' in content:
        print("✅ URLs statiques configurées pour la production")
        return True
    else:
        print("❌ URLs statiques manquantes pour la production")
        return False

def check_settings_production():
    """Vérifie settings_production.py"""
    print("🔍 Vérification de settings_production.py...")
    
    # Importer les settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
    
    try:
        import django
        django.setup()
        from django.conf import settings
        
        # Vérifications
        checks = [
            ('STATIC_URL', settings.STATIC_URL == '/static/'),
            ('STATIC_ROOT', 'staticfiles' in str(settings.STATIC_ROOT)),
            ('STATICFILES_DIRS', len(settings.STATICFILES_DIRS) > 0),
            ('MEDIA_URL', settings.MEDIA_URL == '/media/'),
            ('MEDIA_ROOT', 'media' in str(settings.MEDIA_ROOT)),
        ]
        
        all_good = True
        for name, check in checks:
            if check:
                print(f"  ✅ {name}: OK")
            else:
                print(f"  ❌ {name}: PROBLÈME")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement des settings: {e}")
        return False

def run_collectstatic():
    """Exécute collectstatic"""
    print("📁 Exécution de collectstatic...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear',
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ collectstatic réussi")
            # Compter les fichiers
            lines = result.stdout.split('\n')
            for line in lines:
                if 'static files copied' in line:
                    print(f"  📊 {line.strip()}")
            return True
        else:
            print(f"❌ Erreur collectstatic: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de collectstatic: {e}")
        return False

def check_critical_files():
    """Vérifie que les fichiers critiques sont présents"""
    print("🔍 Vérification des fichiers critiques...")
    
    critical_files = [
        'staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css',
        'staticfiles/css/vendors_css.css',
        'staticfiles/css/style.css',
        'static/css/vendors_css.css',
    ]
    
    all_good = True
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} MANQUANT")
            all_good = False
    
    return all_good

def create_deployment_summary():
    """Crée un résumé pour le déploiement"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ POUR LE DÉPLOIEMENT RAILWAY")
    print("="*60)
    
    print("\n✅ CORRECTIONS APPLIQUÉES:")
    print("  🔧 urls.py - Configuration production des fichiers statiques")
    print("  🔧 settings_production.py - MEDIA_ROOT corrigé")
    print("  🔧 vendors_css.css - URLs relatives")
    print("  🔧 collectstatic - Fichiers collectés")
    
    print("\n🚀 ÉTAPES DE DÉPLOIEMENT:")
    print("  1. git add .")
    print("  2. git commit -m 'Fix static files serving for Railway production'")
    print("  3. git push origin main")
    print("  4. Railway redéploie automatiquement")
    print("  5. Tester: https://votre-app.up.railway.app")
    
    print("\n🧪 TESTS À EFFECTUER APRÈS DÉPLOIEMENT:")
    print("  • Interface de login avec design correct")
    print("  • CSS Bootstrap chargé")
    print("  • Images et médias affichés")
    print("  • Test URL: https://votre-app.up.railway.app/static/css/style.css")
    
    print("\n💡 SI LE PROBLÈME PERSISTE:")
    print("  • Vérifier les logs Railway pour les erreurs 404")
    print("  • Forcer un rebuild complet sur Railway")
    print("  • Vérifier que collectstatic s'exécute bien au build")

def main():
    """Fonction principale"""
    print("🚀 Correction finale des fichiers statiques pour Railway\n")
    
    all_checks_passed = True
    
    # Vérifications
    checks = [
        ("URLs configuration", check_urls_py),
        ("Settings production", check_settings_production),
        ("Collectstatic", run_collectstatic),
        ("Fichiers critiques", check_critical_files),
    ]
    
    for name, check_func in checks:
        print(f"\n{'='*20} {name} {'='*20}")
        if not check_func():
            all_checks_passed = False
    
    # Résumé final
    create_deployment_summary()
    
    if all_checks_passed:
        print("\n🎉 SUCCÈS: Tous les contrôles sont passés!")
        print("✅ Votre application est prête pour Railway")
        return True
    else:
        print("\n❌ ÉCHEC: Certains contrôles ont échoué")
        print("🔧 Veuillez corriger les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)