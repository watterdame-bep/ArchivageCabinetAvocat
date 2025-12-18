#!/usr/bin/env python
"""
Script pour vérifier et lister les templates JSReport disponibles
"""
import requests
import json
from datetime import datetime

def check_jsreport_server(url, username=None, password=None):
    """Vérifie un serveur JSReport et liste ses templates"""
    print(f"🔍 Vérification du serveur: {url}")
    print("-" * 50)
    
    # Headers d'authentification
    headers = {'Content-Type': 'application/json'}
    auth = None
    if username and password:
        auth = (username, password)
        print(f"🔐 Authentification: {username}")
    
    try:
        # Test de connexion
        response = requests.get(f"{url}/api/ping", auth=auth, timeout=10)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Serveur non accessible (Status: {response.status_code})")
            return False
        
        # Récupérer les templates
        response = requests.get(f"{url}/odata/templates", auth=auth, timeout=10)
        response.raise_for_status()
        
        templates = response.json().get('value', [])
        print(f"📋 Nombre de templates: {len(templates)}")
        
        if templates:
            print("\n📄 Templates disponibles:")
            for i, template in enumerate(templates, 1):
                name = template.get('name', 'Sans nom')
                engine = template.get('engine', 'Inconnu')
                recipe = template.get('recipe', 'Inconnu')
                modified = template.get('modificationDate', 'Inconnu')
                
                print(f"   {i}. {name}")
                print(f"      Engine: {engine} | Recipe: {recipe}")
                print(f"      Modifié: {modified}")
                print()
        else:
            print("⚠️  Aucun template trouvé")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout de connexion")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erreur HTTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def compare_servers():
    """Compare les templates entre local et production"""
    print("🔄 Comparaison des Templates JSReport")
    print("=" * 60)
    
    # Serveur local
    print("🏠 SERVEUR LOCAL")
    local_ok = check_jsreport_server("http://localhost:5488")
    
    if not local_ok:
        print("\n💡 Pour démarrer JSReport local:")
        print("   docker run -p 5488:5488 jsreport/jsreport:4.7.0")
        return
    
    print("\n" + "=" * 60)
    
    # Serveur production
    prod_url = input("🌐 URL JSReport production (ou Enter pour passer): ").strip()
    if prod_url:
        print(f"\n🌐 SERVEUR PRODUCTION")
        username = input("👤 Username (défaut: admin): ").strip() or "admin"
        password = input("🔒 Password: ").strip()
        
        if password:
            check_jsreport_server(prod_url, username, password)
        else:
            print("⚠️  Pas de mot de passe fourni, vérification ignorée")

def export_templates_info():
    """Exporte les informations des templates locaux"""
    print("💾 Export des informations des templates")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:5488/odata/templates", timeout=10)
        response.raise_for_status()
        
        templates = response.json().get('value', [])
        
        if not templates:
            print("⚠️  Aucun template à exporter")
            return
        
        # Créer un rapport détaillé
        report = {
            'export_date': datetime.now().isoformat(),
            'server_url': 'http://localhost:5488',
            'templates_count': len(templates),
            'templates': []
        }
        
        for template in templates:
            template_info = {
                'name': template.get('name'),
                'engine': template.get('engine'),
                'recipe': template.get('recipe'),
                'modificationDate': template.get('modificationDate'),
                'id': template.get('_id')
            }
            report['templates'].append(template_info)
        
        # Sauvegarder le rapport
        filename = f"jsreport_templates_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Rapport sauvegardé: {filename}")
        print(f"📊 {len(templates)} template(s) documenté(s)")
        
        # Afficher le résumé
        print("\n📋 Résumé des templates:")
        for template in report['templates']:
            print(f"   • {template['name']} ({template['engine']})")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")

def main():
    """Menu principal"""
    print("🧪 Vérificateur de Templates JSReport")
    print("=" * 60)
    
    while True:
        print("\n📋 Options disponibles:")
        print("1. Vérifier JSReport local")
        print("2. Comparer local et production")
        print("3. Exporter infos templates locaux")
        print("4. Quitter")
        
        choice = input("\n🎯 Votre choix (1-4): ").strip()
        
        if choice == '1':
            print("\n🏠 VÉRIFICATION LOCAL")
            check_jsreport_server("http://localhost:5488")
            
        elif choice == '2':
            compare_servers()
            
        elif choice == '3':
            export_templates_info()
            
        elif choice == '4':
            print("👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()