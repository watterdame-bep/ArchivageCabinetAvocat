#!/usr/bin/env python3
"""
Script pour tester la connexion au service JSReport Railway
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

# Configuration JSReport
JSREPORT_URL = os.getenv("JSREPORT_SERVICE_URL", "")
JSREPORT_USER = os.getenv("JSREPORT_USERNAME", "admin")
JSREPORT_PASSWORD = os.getenv("JSREPORT_PASSWORD", "")

def test_jsreport_connection():
    """Tester la connexion au service JSReport"""
    print("🔍 Test de connexion JSReport Railway")
    print("=" * 50)
    
    # Vérifier la configuration
    if not JSREPORT_URL:
        print("❌ JSREPORT_SERVICE_URL non configurée")
        print("   Exemple: export JSREPORT_SERVICE_URL='https://votre-service.up.railway.app'")
        return False
    
    if not JSREPORT_PASSWORD:
        print("❌ JSREPORT_PASSWORD non configurée")
        print("   Exemple: export JSREPORT_PASSWORD='votre-mot-de-passe'")
        return False
    
    print(f"🌐 URL JSReport: {JSREPORT_URL}")
    print(f"👤 Utilisateur: {JSREPORT_USER}")
    print(f"🔑 Mot de passe: {'*' * len(JSREPORT_PASSWORD)}")
    
    try:
        # Test de connexion basique
        print("\n🔗 Test de connexion...")
        auth = HTTPBasicAuth(JSREPORT_USER, JSREPORT_PASSWORD)
        response = requests.get(f"{JSREPORT_URL.rstrip('/')}/api/templates", auth=auth, timeout=10)
        
        if response.status_code == 200:
            templates = response.json()
            print(f"✅ Connexion réussie!")
            print(f"📄 Nombre de templates: {len(templates)}")
            
            if templates:
                print("\n📋 Templates disponibles:")
                for template in templates:
                    print(f"   - {template.get('name', 'Sans nom')}")
            else:
                print("⚠️  Aucun template trouvé")
            
            return True
            
        elif response.status_code == 401:
            print("❌ Erreur d'authentification (401)")
            print("   Vérifiez JSREPORT_USERNAME et JSREPORT_PASSWORD")
            return False
            
        elif response.status_code == 404:
            print("❌ Service non trouvé (404)")
            print("   Vérifiez JSREPORT_SERVICE_URL")
            return False
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au service")
        print("   Vérifiez que le service JSReport est démarré")
        print(f"   URL: {JSREPORT_URL}")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Timeout de connexion")
        print("   Le service JSReport met trop de temps à répondre")
        return False
        
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

def test_template_creation():
    """Tester la création d'un template de test"""
    print("\n🧪 Test de création de template...")
    
    try:
        auth = HTTPBasicAuth(JSREPORT_USER, JSREPORT_PASSWORD)
        
        # Template de test simple
        test_template = {
            "name": "test_connection",
            "content": "<h1>Test de connexion réussi!</h1><p>{{message}}</p>",
            "engine": "handlebars",
            "recipe": "chrome-pdf"
        }
        
        # Créer le template
        response = requests.post(
            f"{JSREPORT_URL.rstrip('/')}/api/templates",
            json=test_template,
            auth=auth,
            timeout=10
        )
        
        if response.status_code in (200, 201):
            print("✅ Création de template réussie")
            
            # Supprimer le template de test
            template_data = response.json()
            template_id = template_data.get('_id')
            
            if template_id:
                delete_response = requests.delete(
                    f"{JSREPORT_URL.rstrip('/')}/api/templates/{template_id}",
                    auth=auth,
                    timeout=10
                )
                
                if delete_response.status_code in (200, 204):
                    print("✅ Suppression de template de test réussie")
                else:
                    print("⚠️  Template de test créé mais non supprimé")
            
            return True
            
        else:
            print(f"❌ Erreur création template: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test création: {str(e)}")
        return False

def main():
    """Fonction principale"""
    success = test_jsreport_connection()
    
    if success:
        success = test_template_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tous les tests JSReport sont passés!")
        print("✅ Votre service JSReport est prêt pour le déploiement")
        return 0
    else:
        print("❌ Des erreurs ont été détectées")
        print("🔧 Corrigez la configuration avant de continuer")
        return 1

if __name__ == "__main__":
    sys.exit(main())