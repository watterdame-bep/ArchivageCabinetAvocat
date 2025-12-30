#!/usr/bin/env python3
"""
Script pour récupérer automatiquement les templates depuis JSReport local
et les sauvegarder dans le dossier templates_jsreport
"""

import os
import sys
import json
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

# Configuration JSReport local
JSREPORT_LOCAL_URL = os.getenv("JSREPORT_LOCAL_URL", "http://localhost:5488")
JSREPORT_LOCAL_USER = os.getenv("JSREPORT_LOCAL_USERNAME", "admin")
JSREPORT_LOCAL_PASSWORD = os.getenv("JSREPORT_LOCAL_PASSWORD", "")

# Dossier de destination
TEMPLATES_DIR = Path(__file__).parent.parent / "templates_jsreport"

class JSReportDownloader:
    def __init__(self, url, username, password):
        self.url = url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password) if password else None
        self.session = requests.Session()
        if self.auth:
            self.session.auth = self.auth
        
    def test_connection(self):
        """Tester la connexion au JSReport local"""
        try:
            response = self.session.get(f"{self.url}/api/templates")
            if response.status_code == 200:
                print(f"✅ Connexion JSReport local réussie : {self.url}")
                return True
            else:
                print(f"❌ Erreur de connexion JSReport local : {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Impossible de se connecter à JSReport local : {str(e)}")
            print("   Vérifiez que JSReport local est démarré sur http://localhost:5488")
            return False
    
    def get_templates(self):
        """Récupérer tous les templates depuis JSReport local"""
        try:
            response = self.session.get(f"{self.url}/api/templates")
            if response.status_code == 200:
                templates = response.json()
                print(f"📋 Trouvé {len(templates)} template(s) dans JSReport local")
                return templates
            else:
                print(f"❌ Erreur récupération templates : {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur récupération templates : {str(e)}")
            return []
    
    def save_template(self, template):
        """Sauvegarder un template dans le dossier local"""
        template_name = template.get('name', 'unnamed_template')
        
        # Nettoyer le nom du fichier
        safe_name = "".join(c for c in template_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        try:
            # Sauvegarder le contenu HTML
            html_file = TEMPLATES_DIR / f"{safe_name}.html"
            html_content = template.get('content', '')
            
            if html_content:
                html_file.write_text(html_content, encoding='utf-8')
                print(f"💾 Sauvegardé : {html_file.name}")
            else:
                print(f"⚠️  Template '{template_name}' sans contenu HTML")
                return False
            
            # Sauvegarder la configuration JSON
            config = {
                "name": template_name,
                "engine": template.get('engine', 'handlebars'),
                "recipe": template.get('recipe', 'chrome-pdf'),
                "helpers": template.get('helpers', ''),
            }
            
            # Ajouter les configurations spécifiques si présentes
            for key in ['phantom', 'chrome', 'pdf', 'data']:
                if key in template and template[key]:
                    config[key] = template[key]
            
            # Ajouter les métadonnées
            if 'modificationDate' in template:
                config['modificationDate'] = template['modificationDate']
            if 'creationDate' in template:
                config['creationDate'] = template['creationDate']
            
            # Sauvegarder le fichier de configuration
            json_file = TEMPLATES_DIR / f"{safe_name}.json"
            json_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"⚙️  Configuration : {json_file.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde '{template_name}' : {str(e)}")
            return False

def main():
    print("📥 Récupération des templates JSReport locaux")
    print("=" * 50)
    
    # Créer le dossier de destination s'il n'existe pas
    TEMPLATES_DIR.mkdir(exist_ok=True)
    
    # Vérifier s'il y a déjà des fichiers
    existing_files = list(TEMPLATES_DIR.glob("*"))
    if existing_files:
        print(f"⚠️  Le dossier contient déjà {len(existing_files)} fichier(s)")
        response = input("   Continuer et écraser les fichiers existants ? (y/N): ")
        if response.lower() not in ['y', 'yes', 'o', 'oui']:
            print("❌ Opération annulée")
            return 0
    
    # Initialiser le downloader
    downloader = JSReportDownloader(JSREPORT_LOCAL_URL, JSREPORT_LOCAL_USER, JSREPORT_LOCAL_PASSWORD)
    
    # Tester la connexion
    if not downloader.test_connection():
        print("\n💡 Conseils de dépannage :")
        print("   1. Vérifiez que JSReport est démarré : npm start jsreport")
        print("   2. Vérifiez l'URL : http://localhost:5488")
        print("   3. Vérifiez les credentials si vous avez configuré l'authentification")
        return 1
    
    # Récupérer les templates
    templates = downloader.get_templates()
    if not templates:
        print("❌ Aucun template trouvé dans JSReport local")
        return 1
    
    # Afficher la liste des templates trouvés
    print(f"\n📋 Templates trouvés :")
    for i, template in enumerate(templates, 1):
        name = template.get('name', 'Sans nom')
        engine = template.get('engine', 'N/A')
        recipe = template.get('recipe', 'N/A')
        print(f"   {i}. {name} ({engine} → {recipe})")
    
    # Demander confirmation
    response = input(f"\n📥 Télécharger ces {len(templates)} template(s) ? (Y/n): ")
    if response.lower() in ['n', 'no', 'non']:
        print("❌ Opération annulée")
        return 0
    
    # Sauvegarder tous les templates
    print(f"\n💾 Sauvegarde des templates...")
    success_count = 0
    
    for template in templates:
        if downloader.save_template(template):
            success_count += 1
        print()  # Ligne vide pour la lisibilité
    
    # Résumé
    print("=" * 50)
    print(f"✅ Récupération terminée : {success_count}/{len(templates)} templates sauvegardés")
    print(f"📁 Emplacement : {TEMPLATES_DIR}")
    
    if success_count > 0:
        print(f"\n🚀 Prochaines étapes :")
        print(f"   1. Vérifiez les templates dans : {TEMPLATES_DIR}")
        print(f"   2. Modifiez-les si nécessaire")
        print(f"   3. Utilisez upload_jsreport_templates.py pour les envoyer vers Railway")
    
    return 0 if success_count == len(templates) else 1

if __name__ == "__main__":
    sys.exit(main())