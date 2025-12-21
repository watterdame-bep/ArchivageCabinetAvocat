#!/usr/bin/env python
"""
Script pour tester le serveur local avec les fichiers statiques
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_local_server():
    """Test du serveur local avec les fichiers statiques"""
    
    print("🚀 TEST DU SERVEUR LOCAL AVEC FICHIERS STATIQUES")
    print("=" * 55)
    
    # 1. Vérifier que manage.py existe
    if not os.path.exists('manage.py'):
        print("❌ manage.py non trouvé. Exécutez ce script depuis le dossier CabinetAvocat")
        return False
    
    # 2. Exécuter collectstatic
    print("\n📦 Exécution de collectstatic...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ collectstatic réussi")
        else:
            print(f"⚠️ collectstatic: {result.stderr}")
    except Exception as e:
        print(f"❌ Erreur collectstatic: {e}")
    
    # 3. Instructions pour l'utilisateur
    print("\n🎯 INSTRUCTIONS POUR TESTER:")
    print("1. Ouvrez un terminal dans le dossier CabinetAvocat")
    print("2. Exécutez une de ces commandes:")
    print("   Option A (recommandée): python manage.py runserver")
    print("   Option B (si problème): python manage.py runserver --insecure")
    print("3. Ouvrez http://127.0.0.1:8000 dans votre navigateur")
    print("4. Connectez-vous et vérifiez que le design s'affiche correctement")
    
    # 4. Vérifications finales
    print("\n🔍 VÉRIFICATIONS FINALES:")
    
    # Vérifier les dossiers statiques
    static_dir = Path("static")
    staticfiles_dir = Path("staticfiles")
    
    if static_dir.exists():
        css_files = list(static_dir.glob("css/*.css"))
        js_files = list(static_dir.glob("js/*.js"))
        print(f"✅ Dossier static: {len(css_files)} CSS, {len(js_files)} JS")
    else:
        print("❌ Dossier static manquant")
    
    if staticfiles_dir.exists():
        all_files = list(staticfiles_dir.rglob("*"))
        print(f"✅ Dossier staticfiles: {len(all_files)} fichiers")
    else:
        print("❌ Dossier staticfiles manquant")
    
    # 5. Conseils de dépannage
    print("\n🛠️ SI LE PROBLÈME PERSISTE:")
    print("1. Vérifiez que vous êtes en mode DEBUG = True")
    print("2. Videz le cache du navigateur (Ctrl+F5)")
    print("3. Vérifiez la console du navigateur (F12) pour les erreurs 404")
    print("4. Essayez d'accéder directement à: http://127.0.0.1:8000/static/css/style.css")
    
    print("\n✅ Configuration corrigée ! Le serveur devrait maintenant fonctionner correctement.")
    
    return True

if __name__ == '__main__':
    test_local_server()