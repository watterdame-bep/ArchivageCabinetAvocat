#!/usr/bin/env python3
"""
Script pour uploader automatiquement les templates JSReport locaux 
vers le service JSReport Railway en ligne
"""

import os
import sys
import json
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

# Ajouter le répertoire parent au PYTHONPATH pour importer Django
sys.path.append(str(Path(__file__).parent.parent))

# Configuration JSReport
JSREPORT_URL = os.getenv("JSREPORT_SERVICE_URL", "https://votre-jsreport-service.up.railway.app")
JSREPORT_USER = os.getenv("JSREPORT_USERNAME", "admin")
JSREPORT_PASSWORD = os.getenv("JSREPORT_PASSWORD", "")

# Dossier contenant les templates locaux
TEMPLATES_DIR = Path(__file__).parent.parent / "templates_jsreport"

class JSReportUploader:
    def __init__(self, url, username, password):
        self.url = url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        
    def test_connection(self):
        """Tester la connexion au service JSReport"""
        try:
            response = self.session.get(f"{self.url}/api/templates")
            if response.status_code == 200:
                print(f"✅ Connexion JSReport réussie : {self.url}")
                return True
            else:
                print(f"❌ Erreur de connexion JSReport : {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Impossible de se connecter à JSReport : {str(e)}")
            return False
    
    def get_existing_templates(self):
        """Récupérer la liste des templates existants"""
        try:
            response = self.session.get(f"{self.url}/api/templates")
            if response.status_code == 200:
                templates = response.json()
                return {t['name']: t['_id'] for t in templates}
            return {}
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des templates : {str(e)}")
            return {}
    
    def delete_template(self, template_id, template_name):
        """Supprimer un template existant"""
        try:
            response = self.session.delete(f"{self.url}/api/templates/{template_id}")
            if response.status_code in (200, 204):
                print(f"🗑️  Template '{template_name}' supprimé")
                return True
            else:
                print(f"⚠️  Erreur suppression '{template_name}' : {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur suppression '{template_name}' : {str(e)}")
            return False
    
    def upload_template(self, template_file):
        """Upload un template JSReport"""
        template_name = template_file.stem
        
        try:
            # Lire le contenu du template
            content = template_file.read_text(encoding="utf-8")
            
            # Chercher un fichier de configuration JSON associé
            config_file = template_file.with_suffix('.json')
            template_config = {}
            
            if config_file.exists():
                try:
                    template_config = json.loads(config_file.read_text(encoding="utf-8"))
                    print(f"📄 Configuration trouvée pour '{template_name}'")
                except json.JSONDecodeError:
                    print(f"⚠️  Configuration JSON invalide pour '{template_name}'")
            
            # Préparer le payload
            payload = {
                "name": template_name,
                "content": content,
                "engine": template_config.get("engine", "handlebars"),
                "recipe": template_config.get("recipe", "chrome-pdf"),
                "helpers": template_config.get("helpers", ""),
                "phantom": template_config.get("phantom", {}),
                "chrome": template_config.get("chrome", {
                    "format": "A4",
                    "marginTop": "1cm",
                    "marginBottom": "1cm",
                    "marginLeft": "1cm",
                    "marginRight": "1cm"
                })
            }
            
            # Ajouter d'autres propriétés si présentes dans la config
            for key in ["data", "phantom", "chrome", "pdf"]:
                if key in template_config:
                    payload[key] = template_config[key]
            
            # Envoyer le template
            response = self.session.post(f"{self.url}/api/templates", json=payload)
            
            if response.status_code in (200, 201):
                print(f"✅ Template '{template_name}' uploadé avec succès")
                return True
            else:
                print(f"❌ Erreur upload '{template_name}' : {response.status_code}")
                print(f"   Réponse : {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur upload '{template_name}' : {str(e)}")
            return False

def main():
    print("🚀 Upload des templates JSReport vers Railway")
    print("=" * 50)
    
    # Vérifier la configuration
    if not JSREPORT_URL or JSREPORT_URL == "https://votre-jsreport-service.up.railway.app":
        print("❌ JSREPORT_SERVICE_URL non configurée")
        print("   Exemple: export JSREPORT_SERVICE_URL='https://votre-service.up.railway.app'")
        print("   Ou créez un fichier .env avec JSREPORT_SERVICE_URL=...")
        return 1
    
    if not JSREPORT_PASSWORD:
        print("❌ JSREPORT_PASSWORD non configurée")
        print("   Exemple: export JSREPORT_PASSWORD='votre-mot-de-passe'")
        print("   Ou créez un fichier .env avec JSREPORT_PASSWORD=...")
        return 1
    
    # Vérifier que le dossier templates existe
    if not TEMPLATES_DIR.exists():
        print(f"❌ Dossier templates non trouvé : {TEMPLATES_DIR}")
        print("   Créez le dossier templates_jsreport et ajoutez vos templates HTML")
        return 1
    
    print(f"🌐 Service JSReport: {JSREPORT_URL}")
    print(f"👤 Utilisateur: {JSREPORT_USER}")
    print(f"📁 Dossier templates: {TEMPLATES_DIR}")
    
    # Initialiser l'uploader
    uploader = JSReportUploader(JSREPORT_URL, JSREPORT_USER, JSREPORT_PASSWORD)
    
    # Tester la connexion
    if not uploader.test_connection():
        print("\n💡 Conseils de dépannage:")
        print("   1. Vérifiez que le service JSReport est démarré")
        print("   2. Vérifiez l'URL du service (doit commencer par https://)")
        print("   3. Vérifiez les identifiants (username/password)")
        print("   4. Testez avec: python scripts/test_jsreport_connection.py")
        return 1
    
    # Récupérer les templates existants
    print("\n📋 Récupération des templates existants...")
    existing_templates = uploader.get_existing_templates()
    if existing_templates:
        print(f"   Trouvé {len(existing_templates)} template(s) existant(s):")
        for name in existing_templates.keys():
            print(f"     - {name}")
    else:
        print("   Aucun template existant")
    
    # Trouver les templates à uploader
    template_files = list(TEMPLATES_DIR.glob("*.html"))
    if not template_files:
        print(f"❌ Aucun template HTML trouvé dans {TEMPLATES_DIR}")
        print("   Ajoutez vos fichiers .html dans ce dossier")
        return 1
    
    print(f"\n📁 Templates à uploader ({len(template_files)}):")
    for template_file in template_files:
        config_file = template_file.with_suffix('.json')
        config_status = "✅" if config_file.exists() else "⚠️ "
        print(f"   {config_status} {template_file.name}")
    
    # Demander confirmation pour supprimer les existants
    if existing_templates:
        print(f"\n⚠️  {len(existing_templates)} template(s) existant(s) seront remplacés")
        response = input("   Continuer ? (y/N): ")
        if response.lower() not in ['y', 'yes', 'o', 'oui']:
            print("❌ Upload annulé par l'utilisateur")
            return 1
        
        print("\n🗑️  Suppression des templates existants...")
        for name, template_id in existing_templates.items():
            uploader.delete_template(template_id, name)
    
    # Upload des nouveaux templates
    print(f"\n⬆️  Upload des templates...")
    success_count = 0
    failed_templates = []
    
    for template_file in template_files:
        print(f"\n📄 Upload de {template_file.name}...")
        if uploader.upload_template(template_file):
            success_count += 1
        else:
            failed_templates.append(template_file.name)
    
    # Résumé détaillé
    print("\n" + "=" * 50)
    print(f"📊 Résumé de l'upload:")
    print(f"   ✅ Réussis: {success_count}/{len(template_files)}")
    
    if failed_templates:
        print(f"   ❌ Échecs: {len(failed_templates)}")
        print("   Templates en échec:")
        for template in failed_templates:
            print(f"     - {template}")
    
    if success_count == len(template_files):
        print("\n🎉 Tous les templates ont été uploadés avec succès !")
        print("✅ Votre service JSReport est prêt pour la production")
        return 0
    else:
        print(f"\n⚠️  {len(failed_templates)} template(s) n'ont pas pu être uploadés")
        print("🔧 Vérifiez les erreurs ci-dessus et réessayez")
        return 1

if __name__ == "__main__":
    sys.exit(main())