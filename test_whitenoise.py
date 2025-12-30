#!/usr/bin/env python3
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
    print("🧪 Test complet de la configuration WhiteNoise\n")
    
    tests = [
        ("Collectstatic", test_collectstatic),
        ("Serving WhiteNoise", test_whitenoise_serving),
    ]
    
    all_success = True
    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        if not test_func():
            all_success = False
    
    if all_success:
        print("\n🎉 SUCCÈS: WhiteNoise est correctement configuré!")
        print("✅ Prêt pour le déploiement Railway")
    else:
        print("\n❌ ÉCHEC: Problèmes détectés avec WhiteNoise")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
