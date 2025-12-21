#!/usr/bin/env python
"""
Script final pour corriger les fichiers statiques
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def fix_static_files():
    """Correction finale des fichiers statiques"""
    
    print("🔧 CORRECTION FINALE DES FICHIERS STATIQUES")
    print("=" * 50)
    
    # 1. Vérifier qu'on est dans le bon dossier
    if not os.path.exists('manage.py'):
        print("❌ Erreur: Exécutez ce script depuis le dossier CabinetAvocat")
        return False
    
    print("✅ Dossier correct détecté")
    
    # 2. Nettoyer les anciens fichiers statiques
    print("\n🧹 NETTOYAGE DES ANCIENS FICHIERS...")
    
    staticfiles_dir = Path("staticfiles")
    if staticfiles_dir.exists():
        try:
            shutil.rmtree(staticfiles_dir)
            print("✅ Ancien dossier staticfiles supprimé")
        except Exception as e:
            print(f"⚠️ Impossible de supprimer staticfiles: {e}")
    
    # 3. Nettoyer les fichiers Python compilés
    print("\n🧹 NETTOYAGE DES FICHIERS PYTHON...")
    
    try:
        # Supprimer les fichiers .pyc
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.pyc'):
                    os.remove(os.path.join(root, file))
        
        # Supprimer les dossiers __pycache__
        for root, dirs, files in os.walk('.', topdown=False):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    shutil.rmtree(os.path.join(root, dir_name))
        
        print("✅ Fichiers Python compilés nettoyés")
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage: {e}")
    
    # 4. Exécuter collectstatic
    print("\n📦 COLLECTE DES FICHIERS STATIQUES...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ collectstatic réussi")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ collectstatic échoué: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erreur lors de collectstatic: {e}")
    
    # 5. Vérifier que les fichiers sont bien là
    print("\n🔍 VÉRIFICATION DES FICHIERS...")
    
    critical_files = [
        "static/css/style.css",
        "static/css/vendors_css.css",
        "static/js/vendors.min.js",
        "staticfiles/css/style.css",
        "staticfiles/css/vendors_css.css",
        "staticfiles/js/vendors.min.js"
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} manquant")
    
    # 6. Créer un script de démarrage optimisé
    print("\n📝 CRÉATION DU SCRIPT DE DÉMARRAGE...")
    
    start_script = """@echo off
echo 🚀 Démarrage du serveur Django avec fichiers statiques
echo.

echo 📦 Collecte des fichiers statiques...
python manage.py collectstatic --noinput

echo.
echo 🌐 Démarrage du serveur...
echo Ouvrez votre navigateur sur: http://127.0.0.1:8000
echo.
echo ⚠️ Si les styles ne s'affichent pas:
echo 1. Appuyez sur Ctrl+F5 pour vider le cache
echo 2. Ou fermez ce serveur et exécutez: python manage.py runserver --insecure
echo.

python manage.py runserver
"""
    
    with open("start_with_static.bat", "w", encoding="utf-8") as f:
        f.write(start_script)
    
    print("✅ Script start_with_static.bat créé")
    
    # 7. Instructions finales
    print("\n🎯 INSTRUCTIONS FINALES:")
    print("1. Fermez tous les serveurs Django en cours")
    print("2. Exécutez UNE de ces commandes:")
    print("   Option A: start_with_static.bat")
    print("   Option B: python manage.py runserver")
    print("   Option C: python manage.py runserver --insecure")
    print("\n3. Ouvrez http://127.0.0.1:8000")
    print("4. Si les styles ne s'affichent pas:")
    print("   - Appuyez sur Ctrl+F5 (vider le cache)")
    print("   - Ou essayez un autre navigateur")
    print("   - Ou utilisez l'option C ci-dessus")
    
    # 8. Test final
    print("\n🧪 TEST FINAL:")
    print("Pour tester si tout fonctionne:")
    print("1. Ouvrez http://127.0.0.1:8000/static/css/style.css")
    print("2. Vous devriez voir le contenu CSS, pas une erreur 404")
    
    print("\n🎉 CORRECTION TERMINÉE !")
    print("Votre configuration est maintenant optimisée.")
    
    return True

if __name__ == '__main__':
    fix_static_files()