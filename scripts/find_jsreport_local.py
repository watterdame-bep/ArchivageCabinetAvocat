#!/usr/bin/env python3
"""
Script pour détecter JSReport local sur différents ports
"""

import requests
from requests.auth import HTTPBasicAuth

# Ports communs pour JSReport
COMMON_PORTS = [5488, 3000, 8080, 8000, 5000]
COMMON_HOSTS = ['localhost', '127.0.0.1']

def test_jsreport_connection(host, port, username=None, password=None):
    """Tester une connexion JSReport"""
    url = f"http://{host}:{port}"
    
    try:
        auth = HTTPBasicAuth(username, password) if username and password else None
        response = requests.get(f"{url}/api/templates", auth=auth, timeout=5)
        
        if response.status_code == 200:
            return True, url, response.json()
        elif response.status_code == 401:
            return "auth_required", url, None
        else:
            return False, url, None
            
    except requests.exceptions.RequestException:
        return False, url, None

def main():
    print("🔍 Recherche de JSReport local...")
    print("=" * 40)
    
    found_instances = []
    
    for host in COMMON_HOSTS:
        for port in COMMON_PORTS:
            print(f"🔍 Test {host}:{port}...", end=" ")
            
            # Test sans authentification
            result, url, data = test_jsreport_connection(host, port)
            
            if result is True:
                print(f"✅ TROUVÉ ! ({len(data)} templates)")
                found_instances.append({
                    'url': url,
                    'auth_required': False,
                    'templates_count': len(data)
                })
            elif result == "auth_required":
                print("🔐 Authentification requise")
                found_instances.append({
                    'url': url,
                    'auth_required': True,
                    'templates_count': '?'
                })
            else:
                print("❌")
    
    print("\n" + "=" * 40)
    
    if found_instances:
        print(f"✅ JSReport trouvé sur {len(found_instances)} instance(s) :")
        for i, instance in enumerate(found_instances, 1):
            auth_status = "🔐 Auth requise" if instance['auth_required'] else "🔓 Pas d'auth"
            print(f"   {i}. {instance['url']} - {auth_status} - {instance['templates_count']} templates")
        
        print(f"\n💡 Pour récupérer les templates :")
        for instance in found_instances:
            if not instance['auth_required']:
                print(f"   JSREPORT_LOCAL_URL={instance['url']} python scripts/download_local_templates.py")
            else:
                print(f"   JSREPORT_LOCAL_URL={instance['url']} JSREPORT_LOCAL_USERNAME=admin JSREPORT_LOCAL_PASSWORD=votre-password python scripts/download_local_templates.py")
    else:
        print("❌ Aucune instance JSReport trouvée")
        print("\n💡 Vérifiez que JSReport est démarré :")
        print("   - npm start jsreport")
        print("   - jsreport start")
        print("   - ou votre méthode habituelle")

if __name__ == "__main__":
    main()