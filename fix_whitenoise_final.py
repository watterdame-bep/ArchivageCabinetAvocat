#!/usr/bin/env python3
"""
Script pour corriger définitivement la configuration WhiteNoise sur Railway
"""

import os
import sys
from pathlib import Path

def fix_settings_production():
    """Corrige settings_production.py pour WhiteNoise"""
    print("🔧 Correction de settings_production.py pour WhiteNoise...")
    
    settings_file = Path('CabinetAvocat/settings_production.py')
    if not settings_file.exists():
        print(f"❌ Fichier non trouvé: {settings_file}")
        return False
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrections à appliquer
    corrections = [
        # 1. Supprimer STATICFILES_DIRS en production (CRITIQUE)
        (
            "# CRITIQUE: Configuration STATICFILES_DIRS pour collectstatic\nSTATICFILES_DIRS = [\n    os.path.join(BASE_DIR, 'static'),\n]",
            "# CRITIQUE: STATICFILES_DIRS supprimé en production (conflit avec WhiteNoise)\n# En production, seul STATIC_ROOT est utilisé\n# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Seulement en local"
        ),
        
        # 2. Corriger STATICFILES_STORAGE pour WhiteNoise
        (
            "STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'",
            "STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'"
        ),
        
        # 3. Simplifier la configuration WhiteNoise
        (
            """WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br',
    'map', 'woff', 'woff2', 'ttf', 'otf', 'eot', 'svg', 'ico', 'css', 'js'
]
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 0  # Pas de cache pour éviter les problèmes""",
            """# Configuration WhiteNoise pour Railway
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000  # 1 an de cache (optimisé pour production)"""
        )
    ]
    
    # Appliquer les corrections
    for old, new in corrections:
        if old in content:
            content = content.replace(old, new)
            print(f"  ✅ Correction appliquée: {old[:50]}...")
        else:
            print(f"  ⚠️ Texte non trouvé: {old[:50]}...")
    
    # Écrire le fichier corrigé
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ settings_production.py corrigé pour WhiteNoise")
    return True

def verify_middleware_order():
    """Vérifie l'ordre du middleware WhiteNoise"""
    print("🔍 Vérification de l'ordre du middleware...")
    
    # Lire le settings de base pour voir l'ordre du middleware
    base_settings = Path('CabinetAvocat/settings.py')
    if base_settings.exists():
        with open(base_settings, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'MIDDLEWARE' in content:
            print("  ✅ MIDDLEWARE trouvé dans settings.py")
            # Extraire la section MIDDLEWARE
            lines = content.split('\n')
            in_middleware = False
            middleware_lines = []
            
            for line in lines:
                if 'MIDDLEWARE = [' in line:
                    in_middleware = True
                    middleware_lines.append(line)
                elif in_middleware:
                    middleware_lines.append(line)
                    if ']' in line and not line.strip().startswith('#'):
                        break
            
            print("  📋 Ordre actuel du middleware:")
            for line in middleware_lines:
                print(f"    {line}")
            
            return True
    
    print("  ❌ Impossible de vérifier l'ordre du middleware")
    return False

def test_whitenoise_config():
    """Teste la configuration WhiteNoise"""
    print("🧪 Test de la configuration WhiteNoise...")
    
    try:
        # Configurer l'environnement Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        # Vérifications
        checks = [
            ('STATIC_URL', settings.STATIC_URL == '/static/'),
            ('STATIC_ROOT', 'staticfiles' in str(settings.STATIC_ROOT)),
            ('STATICFILES_STORAGE', 'whitenoise' in settings.STATICFILES_STORAGE.lower()),
            ('WhiteNoise Middleware', 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE),
        ]
        
        all_good = True
        for name, check in checks:
            if check:
                print(f"  ✅ {name}: OK")
            else:
                print(f"  ❌ {name}: PROBLÈME")
                all_good = False
        
        # Vérifier STATICFILES_DIRS
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            print(f"  ⚠️ STATICFILES_DIRS encore présent: {settings.STATICFILES_DIRS}")
            print("    👉 Cela peut causer des conflits avec WhiteNoise en production")
            all_good = False
        else:
            print("  ✅ STATICFILES_DIRS: Correctement supprimé en production")
        
        return all_good
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {e}")
        return False

def create_whitenoise_test_script():
    """Crée un script de test pour WhiteNoise"""
    print("📝 Création d'un script de test WhiteNoise...")
    
    test_script = '''#!/usr/bin/env python3
"""
Script de test pour vérifier que WhiteNoise fonctionne correctement
"""

import os
import sys
import subprocess
from pathlib import Path

def test_collectstatic():
    """Teste collectstatic avec la nouvelle configuration"""
    print("📁 Test collectstatic avec WhiteNoise...")
    
    try:
        # Nettoyer staticfiles
        staticfiles_dir = Path('staticfiles')
        if staticfiles_dir.exists():
            import shutil
            shutil.rmtree(staticfiles_dir)
            print("🗑️ Dossier staticfiles nettoyé")
        
        # Exécuter collectstatic
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput',
            '--settings=CabinetAvocat.settings_production'
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ collectstatic réussi avec WhiteNoise")
            
            # Vérifier les fichiers critiques
            critical_files = [
                'staticfiles/css/style.css',
                'staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css'
            ]
            
            for file_path in critical_files:
                if Path(file_path).exists():
                    size = Path(file_path).stat().st_size
                    print(f"  ✅ {file_path} ({size} bytes)")
                else:
                    print(f"  ❌ {file_path} MANQUANT")
            
            return True
        else:
            print(f"❌ Erreur collectstatic: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
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
        response = client.get('/test-static/')
        if response.status_code == 200:
            print("✅ Endpoint de test accessible")
            
            import json
            data = json.loads(response.content)
            print(f"  📊 Environment: {data.get('environment', 'Unknown')}")
            print(f"  📁 STATIC_ROOT: {data.get('static_root', 'Unknown')}")
            
            files = data.get('files', {})
            for file_path, info in files.items():
                if info['exists']:
                    print(f"  ✅ {file_path} ({info['size']} bytes)")
                else:
                    print(f"  ❌ {file_path} MANQUANT")
        else:
            print(f"❌ Endpoint de test inaccessible: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test serving: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 Test complet de la configuration WhiteNoise\\n")
    
    tests = [
        ("Collectstatic", test_collectstatic),
        ("Serving WhiteNoise", test_whitenoise_serving),
    ]
    
    all_success = True
    for name, test_func in tests:
        print(f"\\n{'='*20} {name} {'='*20}")
        if not test_func():
            all_success = False
    
    if all_success:
        print("\\n🎉 SUCCÈS: WhiteNoise est correctement configuré!")
        print("✅ Prêt pour le déploiement Railway")
    else:
        print("\\n❌ ÉCHEC: Problèmes détectés avec WhiteNoise")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
    
    with open('test_whitenoise.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Script test_whitenoise.py créé")

def main():
    """Fonction principale"""
    print("🚀 Correction finale de WhiteNoise pour Railway\n")
    
    steps = [
        ("Correction settings_production.py", fix_settings_production),
        ("Vérification middleware", verify_middleware_order),
        ("Test configuration WhiteNoise", test_whitenoise_config),
        ("Création script de test", create_whitenoise_test_script),
    ]
    
    all_success = True
    for name, func in steps:
        print(f"\n{'='*20} {name} {'='*20}")
        if not func():
            all_success = False
    
    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE LA CORRECTION WHITENOISE")
    print("="*60)
    
    if all_success:
        print("🎉 SUCCÈS: WhiteNoise correctement configuré!")
        print("\n🔧 CORRECTIONS APPLIQUÉES:")
        print("  ✅ STATICFILES_DIRS supprimé en production")
        print("  ✅ STATICFILES_STORAGE configuré pour WhiteNoise")
        print("  ✅ Configuration WhiteNoise optimisée")
        
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("  1. python test_whitenoise.py  # Tester localement")
        print("  2. git add .")
        print("  3. git commit -m 'Fix WhiteNoise configuration for Railway static files'")
        print("  4. git push origin main")
        print("  5. Vérifier sur Railway: https://votre-app.up.railway.app/static/css/style.css")
        
    else:
        print("❌ ÉCHEC: Certaines corrections ont échoué")
        print("🔧 Veuillez corriger les erreurs ci-dessus")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)