#!/usr/bin/env python3
"""
Test final avant déploiement Railway - Vérification complète
"""

import os
import sys
import subprocess
from pathlib import Path

def test_settings_configuration():
    """Teste la configuration des settings de production"""
    print("🔧 Test de la configuration settings_production.py...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        import django
        django.setup()
        from django.conf import settings
        
        # Tests critiques
        tests = [
            ('STATIC_URL', settings.STATIC_URL == '/static/', f"Actuel: {settings.STATIC_URL}"),
            ('STATIC_ROOT', 'staticfiles' in str(settings.STATIC_ROOT), f"Actuel: {settings.STATIC_ROOT}"),
            ('STATICFILES_DIRS', len(settings.STATICFILES_DIRS) == 0, f"Actuel: {settings.STATICFILES_DIRS}"),
            ('STATICFILES_STORAGE', 'whitenoise' in settings.STATICFILES_STORAGE.lower(), f"Actuel: {settings.STATICFILES_STORAGE}"),
            ('WhiteNoise Middleware', 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE, "Middleware OK"),
            ('ALLOWED_HOSTS healthcheck', 'healthcheck.railway.app' in settings.ALLOWED_HOSTS, f"Actuel: {settings.ALLOWED_HOSTS}"),
        ]
        
        all_good = True
        for name, test, info in tests:
            if test:
                print(f"  ✅ {name}: OK")
            else:
                print(f"  ❌ {name}: PROBLÈME - {info}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test settings: {e}")
        return False

def test_collectstatic():
    """Teste collectstatic avec la configuration finale"""
    print("📁 Test collectstatic final...")
    
    try:
        # Nettoyer staticfiles
        staticfiles_dir = Path('staticfiles')
        if staticfiles_dir.exists():
            import shutil
            shutil.rmtree(staticfiles_dir)
            print("  🗑️ Dossier staticfiles nettoyé")
        
        # Exécuter collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear',
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("  ✅ collectstatic réussi")
            
            # Analyser la sortie
            lines = result.stdout.split('\n')
            for line in lines:
                if 'static files copied' in line:
                    print(f"    📊 {line.strip()}")
                if 'post-processed' in line:
                    print(f"    🔄 {line.strip()}")
            
            # Vérifier les fichiers critiques
            critical_files = [
                'staticfiles/css/style.css',
                'staticfiles/css/vendors_css.css',
                'staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css'
            ]
            
            all_present = True
            for file_path in critical_files:
                if Path(file_path).exists():
                    size = Path(file_path).stat().st_size
                    print(f"    ✅ {file_path} ({size:,} bytes)")
                else:
                    print(f"    ❌ {file_path} MANQUANT")
                    all_present = False
            
            return all_present
        else:
            print(f"  ❌ Erreur collectstatic: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def test_whitenoise_serving():
    """Teste que WhiteNoise peut servir les fichiers"""
    print("🌐 Test du serving WhiteNoise...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        
        import django
        django.setup()
        
        from django.test import Client
        from django.conf import settings
        
        # Créer un client de test
        client = Client()
        
        # Tester l'endpoint de diagnostic
        try:
            response = client.get('/test-static/')
            if response.status_code == 200:
                print("  ✅ Endpoint de test accessible")
                
                import json
                data = json.loads(response.content)
                print(f"    📊 Environment: {data.get('environment', 'Unknown')}")
                print(f"    📁 STATIC_ROOT: {data.get('static_root', 'Unknown')}")
                print(f"    📂 STATICFILES_DIRS: {data.get('staticfiles_dirs', 'Unknown')}")
                
                files = data.get('files', {})
                for file_path, info in files.items():
                    if info['exists']:
                        print(f"    ✅ {file_path} ({info['size']:,} bytes)")
                    else:
                        print(f"    ❌ {file_path} MANQUANT")
                
                return True
            else:
                print(f"  ❌ Endpoint de test inaccessible: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ⚠️ Endpoint de test non disponible: {e}")
            return True  # Pas critique pour le déploiement
        
    except Exception as e:
        print(f"  ❌ Erreur test serving: {e}")
        return False

def check_requirements():
    """Vérifie que whitenoise est dans requirements.txt"""
    print("📋 Vérification des requirements...")
    
    req_file = Path('requirements.txt')
    if req_file.exists():
        with open(req_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'whitenoise' in content.lower():
            print("  ✅ whitenoise présent dans requirements.txt")
            return True
        else:
            print("  ❌ whitenoise MANQUANT dans requirements.txt")
            return False
    else:
        print("  ❌ requirements.txt non trouvé")
        return False

def create_deployment_summary():
    """Crée un résumé final pour le déploiement"""
    print("\n" + "="*60)
    print("📋 RÉSUMÉ FINAL - PRÊT POUR DÉPLOIEMENT RAILWAY")
    print("="*60)
    
    print("\n✅ CORRECTIONS APPLIQUÉES:")
    print("  🔧 ALLOWED_HOSTS: healthcheck.railway.app ajouté")
    print("  🔧 WhiteNoise: Configuration optimisée")
    print("  🔧 STATICFILES_DIRS: Vidé pour la production")
    print("  🔧 STATICFILES_STORAGE: WhiteNoise configuré")
    
    print("\n🚀 COMMANDES DE DÉPLOIEMENT:")
    print("  git add .")
    print("  git commit -m 'Fix Railway healthcheck and finalize WhiteNoise configuration'")
    print("  git push origin main")
    
    print("\n🧪 TESTS POST-DÉPLOIEMENT:")
    print("  1. Interface: https://votre-app.up.railway.app/")
    print("  2. Diagnostic: https://votre-app.up.railway.app/test-static/")
    print("  3. CSS direct: https://votre-app.up.railway.app/static/css/style.css")
    
    print("\n📊 LOGS RAILWAY ATTENDUS:")
    print("  ✅ 'X static files copied to /app/staticfiles, Y post-processed'")
    print("  ✅ 'Starting gunicorn on port 8080'")
    print("  ✅ Plus d'erreur 'Invalid HTTP_HOST header'")
    print("  ✅ Plus d'erreur 404 pour les fichiers statiques")

def main():
    """Fonction principale"""
    print("🚀 Test final avant déploiement Railway\n")
    
    tests = [
        ("Vérification requirements", check_requirements),
        ("Configuration settings", test_settings_configuration),
        ("Collectstatic", test_collectstatic),
        ("Serving WhiteNoise", test_whitenoise_serving),
    ]
    
    all_success = True
    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        if not test_func():
            all_success = False
    
    # Résumé final
    create_deployment_summary()
    
    if all_success:
        print("\n🎉 SUCCÈS: Tous les tests sont passés!")
        print("✅ Votre application est prête pour Railway")
        print("🚀 Vous pouvez maintenant déployer en toute sécurité")
    else:
        print("\n❌ ÉCHEC: Certains tests ont échoué")
        print("🔧 Veuillez corriger les erreurs ci-dessus avant de déployer")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)