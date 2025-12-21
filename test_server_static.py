#!/usr/bin/env python
"""
Test du serveur avec accès aux fichiers statiques
"""
import subprocess
import time
import requests
import sys
import os
from threading import Thread

def start_server():
    """Démarre le serveur Django en arrière-plan"""
    try:
        # Démarrer le serveur
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8001'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return None

def test_static_urls():
    """Test des URLs statiques"""
    
    print("🚀 TEST DU SERVEUR AVEC FICHIERS STATIQUES")
    print("=" * 50)
    
    # URLs à tester
    test_urls = [
        ('http://127.0.0.1:8001/static/', 'Index des fichiers statiques'),
        ('http://127.0.0.1:8001/static/css/', 'Dossier CSS'),
        ('http://127.0.0.1:8001/static/css/style.css', 'Fichier CSS principal'),
        ('http://127.0.0.1:8001/static/css/vendors_css.css', 'Fichier CSS vendors'),
        ('http://127.0.0.1:8001/static/js/', 'Dossier JS'),
        ('http://127.0.0.1:8001/static/js/vendors.min.js', 'Fichier JS principal'),
        ('http://127.0.0.1:8001/static/images/favicon.ico', 'Favicon'),
    ]
    
    print("\n🔍 TEST D'ACCÈS AUX FICHIERS:")
    
    for url, description in test_urls:
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                size = len(response.content)
                print(f"✅ {description}")
                print(f"   URL: {url}")
                print(f"   Status: {response.status_code}")
                print(f"   Type: {content_type}")
                print(f"   Taille: {size} bytes")
                
                # Vérifier le contenu pour les fichiers CSS/JS
                if url.endswith('.css'):
                    if 'body' in response.text or 'html' in response.text or '.btn' in response.text:
                        print(f"   ✅ Contenu CSS valide détecté")
                    else:
                        print(f"   ⚠️ Contenu CSS suspect")
                        
                elif url.endswith('.js'):
                    if 'function' in response.text or 'var' in response.text or 'jQuery' in response.text:
                        print(f"   ✅ Contenu JS valide détecté")
                    else:
                        print(f"   ⚠️ Contenu JS suspect")
                        
            elif response.status_code == 404:
                print(f"❌ {description}")
                print(f"   URL: {url}")
                print(f"   Status: 404 - Fichier non trouvé")
                
            else:
                print(f"⚠️ {description}")
                print(f"   URL: {url}")
                print(f"   Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}")
            print(f"   URL: {url}")
            print(f"   Erreur: Impossible de se connecter au serveur")
            
        except Exception as e:
            print(f"❌ {description}")
            print(f"   URL: {url}")
            print(f"   Erreur: {e}")
        
        print()  # Ligne vide pour la lisibilité

def main():
    """Fonction principale"""
    
    print("🎯 INSTRUCTIONS:")
    print("1. Ce script va démarrer un serveur Django sur le port 8001")
    print("2. Il va tester l'accès aux fichiers statiques")
    print("3. Vous pourrez voir exactement quels fichiers sont accessibles")
    print("\n⚠️ IMPORTANT: Fermez tout autre serveur Django avant de continuer")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Démarrer le serveur
    print("\n🚀 Démarrage du serveur...")
    server_process = start_server()
    
    if server_process is None:
        print("❌ Impossible de démarrer le serveur")
        return
    
    try:
        # Tester les URLs
        test_static_urls()
        
        # Instructions finales
        print("\n🎯 RÉSULTATS:")
        print("Si tous les fichiers sont ✅ → Votre configuration est correcte")
        print("Si des fichiers sont ❌ → Il y a un problème de configuration")
        print("\n💡 PROCHAINES ÉTAPES:")
        print("1. Si les fichiers statiques sont accessibles ici,")
        print("   le problème vient probablement des templates")
        print("2. Vérifiez que vos templates utilisent bien {% static 'path' %}")
        print("3. Videz le cache de votre navigateur")
        
    finally:
        # Arrêter le serveur
        print("\n🛑 Arrêt du serveur...")
        server_process.terminate()
        server_process.wait()
        print("✅ Serveur arrêté")

if __name__ == '__main__':
    main()