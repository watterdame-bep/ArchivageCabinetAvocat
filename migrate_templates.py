#!/usr/bin/env python
"""
Script automatisé pour migrer les templates JSReport du local vers la production
"""
import requests
import json
import base64
import os
from datetime import datetime

class JSReportTemplateMigrator:
    def __init__(self, source_url, target_url, target_username=None, target_password=None):
        self.source_url = source_url.rstrip('/')
        self.target_url = target_url.rstrip('/')
        self.target_username = target_username
        self.target_password = target_password
        
    def get_auth_headers(self):
        """Génère les headers d'authentification pour le serveur cible"""
        headers = {'Content-Type': 'application/json'}
        if self.target_username and self.target_password:
            credentials = f"{self.target_username}:{self.target_password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers['Authorization'] = f'Basic {encoded}'
        return headers
    
    def get_templates_from_source(self):
        """Récupère tous les templates du serveur source (local)"""
        try:
            print("📥 Récupération des templates depuis le serveur local...")
            response = requests.get(f"{self.source_url}/odata/templates", timeout=10)
            response.raise_for_status()
            
            templates = response.json().get('value', [])
            print(f"✅ Trouvé {len(templates)} template(s) sur le serveur local")
            
            return templates
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des templates: {e}")
            return []
    
    def get_template_details(self, template_id):
        """Récupère les détails complets d'un template"""
        try:
            # Récupérer le template complet avec son contenu
            response = requests.get(
                f"{self.source_url}/odata/templates({template_id})",
                params={'$expand': 'assets'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du template {template_id}: {e}")
            return None
    
    def create_template_on_target(self, template_data):
        """Crée un template sur le serveur cible"""
        try:
            # Nettoyer les données du template pour la création
            clean_template = {
                'name': template_data['name'],
                'engine': template_data.get('engine', 'handlebars'),
                'recipe': template_data.get('recipe', 'chrome-pdf'),
                'content': template_data.get('content', ''),
                'helpers': template_data.get('helpers', ''),
                'chrome': template_data.get('chrome', {}),
                'phantom': template_data.get('phantom', {})
            }
            
            headers = self.get_auth_headers()
            response = requests.post(
                f"{self.target_url}/odata/templates",
                json=clean_template,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            print(f"✅ Template '{template_data['name']}' créé avec succès")
            return response.json()
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du template '{template_data['name']}': {e}")
            return None
    
    def migrate_templates(self):
        """Migre tous les templates du source vers la cible"""
        print("🚀 Début de la migration des templates JSReport")
        print("=" * 60)
        
        # Vérifier la connexion au serveur cible
        try:
            headers = self.get_auth_headers()
            response = requests.get(f"{self.target_url}/api/ping", headers=headers, timeout=10)
            if response.status_code != 200:
                print("❌ Impossible de se connecter au serveur JSReport cible")
                return False
            print("✅ Connexion au serveur cible réussie")
        except Exception as e:
            print(f"❌ Erreur de connexion au serveur cible: {e}")
            return False
        
        # Récupérer les templates source
        source_templates = self.get_templates_from_source()
        if not source_templates:
            print("❌ Aucun template trouvé sur le serveur source")
            return False
        
        # Migrer chaque template
        success_count = 0
        for template in source_templates:
            print(f"\n📋 Migration du template: {template['name']}")
            
            # Récupérer les détails complets
            template_details = self.get_template_details(template['_id'])
            if not template_details:
                continue
            
            # Créer sur le serveur cible
            if self.create_template_on_target(template_details):
                success_count += 1
        
        print("\n" + "=" * 60)
        print(f"🎯 Migration terminée: {success_count}/{len(source_templates)} templates migrés")
        
        return success_count == len(source_templates)
    
    def backup_templates(self, backup_file="jsreport_templates_backup.json"):
        """Sauvegarde les templates dans un fichier JSON"""
        print(f"💾 Sauvegarde des templates dans {backup_file}...")
        
        templates = self.get_templates_from_source()
        if not templates:
            return False
        
        # Récupérer les détails de chaque template
        detailed_templates = []
        for template in templates:
            details = self.get_template_details(template['_id'])
            if details:
                detailed_templates.append(details)
        
        # Sauvegarder dans un fichier
        backup_data = {
            'export_date': datetime.now().isoformat(),
            'source_url': self.source_url,
            'templates_count': len(detailed_templates),
            'templates': detailed_templates
        }
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Sauvegarde réussie: {len(detailed_templates)} templates dans {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False

def main():
    """Fonction principale de migration"""
    print("🔄 Migration des Templates JSReport")
    print("=" * 60)
    
    # Vérifier que JSReport local est accessible
    print("🔍 Vérification de JSReport local...")
    try:
        response = requests.get("http://localhost:5488/api/ping", timeout=5)
        if response.status_code == 200:
            print("✅ JSReport local accessible")
        else:
            print("❌ JSReport local non accessible")
            print("💡 Démarrez JSReport local avec: docker run -p 5488:5488 jsreport/jsreport:4.7.0")
            return
    except Exception as e:
        print(f"❌ JSReport local non accessible: {e}")
        print("💡 Démarrez JSReport local avec: docker run -p 5488:5488 jsreport/jsreport:4.7.0")
        return
    
    # Configuration
    SOURCE_URL = "http://localhost:5488"  # JSReport local
    TARGET_URL = input("🌐 URL du JSReport de production (ex: https://votre-jsreport.railway.app): ").strip()
    
    if not TARGET_URL:
        print("❌ URL cible requise")
        return
    
    TARGET_USERNAME = input("👤 Username JSReport production (défaut: admin): ").strip() or "admin"
    TARGET_PASSWORD = input("🔒 Password JSReport production: ").strip()
    
    if not TARGET_PASSWORD:
        print("❌ Mot de passe requis")
        return
    
    # Créer le migrateur
    migrator = JSReportTemplateMigrator(
        source_url=SOURCE_URL,
        target_url=TARGET_URL,
        target_username=TARGET_USERNAME,
        target_password=TARGET_PASSWORD
    )
    
    # Proposer une sauvegarde
    backup = input("\n💾 Créer une sauvegarde locale avant migration? (y/N): ").strip().lower()
    if backup in ['y', 'yes', 'oui']:
        migrator.backup_templates()
    
    # Lancer la migration
    print(f"\n🚀 Migration de {SOURCE_URL} vers {TARGET_URL}")
    success = migrator.migrate_templates()
    
    if success:
        print("\n🎉 Migration réussie!")
        print("✅ Tous vos templates sont maintenant disponibles en production")
        print("🧪 N'oubliez pas de tester chaque template dans JSReport Studio")
    else:
        print("\n⚠️ Migration partiellement échouée")
        print("🔧 Vérifiez les erreurs ci-dessus et réessayez si nécessaire")

if __name__ == "__main__":
    main()