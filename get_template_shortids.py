#!/usr/bin/env python
"""
Script pour récupérer les shortids des templates JSReport
"""
import os
import sys
import django
import requests
import json
from base64 import b64encode

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings

def get_jsreport_templates():
    """Récupère tous les templates JSReport avec leurs shortids"""
    print("🔍 RÉCUPÉRATION DES SHORTIDS JSREPORT")
    print("=" * 50)
    
    jsreport_url = getattr(settings, 'JSREPORT_URL', 'http://localhost:5488')
    username = getattr(settings, 'JSREPORT_USERNAME', 'admin')
    password = getattr(settings, 'JSREPORT_PASSWORD', 'admin123')
    
    print(f"URL JSReport: {jsreport_url}")
    
    if 'localhost' in jsreport_url:
        print("⚠️ URL pointe vers localhost - impossible de tester Railway")
        return
    
    try:
        # Authentification
        credentials = f"{username}:{password}"
        auth_header = b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/json'
        }
        
        # Récupérer les templates
        templates_url = f"{jsreport_url}/odata/templates"
        response = requests.get(templates_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            templates = response.json().get('value', [])
            print(f"✅ {len(templates)} template(s) trouvé(s)")
            print()
            
            # Afficher les templates avec leurs shortids
            print("📋 TEMPLATES ET LEURS SHORTIDS:")
            print("-" * 60)
            
            template_mapping = {}
            
            for template in templates:
                name = template.get('name', 'Sans nom')
                shortid = template.get('shortid', 'Pas de shortid')
                recipe = template.get('recipe', 'Pas de recipe')
                
                print(f"📄 Nom: {name}")
                print(f"   🔑 Shortid: {shortid}")
                print(f"   📝 Recipe: {recipe}")
                print()
                
                template_mapping[name] = shortid
            
            # Générer le code Django corrigé
            print("🔧 CODE DJANGO CORRIGÉ:")
            print("-" * 40)
            
            required_templates = [
                "Facture_paiement_client",
                "Facture_dossier", 
                "Extrait_de_compte_client"
            ]
            
            for template_name in required_templates:
                if template_name in template_mapping:
                    shortid = template_mapping[template_name]
                    print(f"# Pour {template_name}")
                    print(f'template_shortid = "{shortid}"')
                    print(f"# Utiliser dans generate_pdf:")
                    print(f"# jsreport_service.generate_pdf_by_shortid('{shortid}', data)")
                    print()
                else:
                    print(f"❌ Template '{template_name}' non trouvé dans JSReport")
                    print(f"   Vérifiez que le template est bien importé")
                    print()
            
            return template_mapping
            
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def generate_updated_service():
    """Génère une version mise à jour du service JSReport"""
    print("\n🔧 SERVICE JSREPORT MIS À JOUR")
    print("=" * 50)
    
    updated_service = '''
# Dans utils/jsreport_service.py - Ajouter cette méthode

def generate_pdf_by_shortid(self, template_shortid: str, data: Dict[str, Any], 
                           options: Optional[Dict[str, Any]] = None) -> Optional[bytes]:
    """
    Génère un PDF via JSReport en utilisant le shortid du template
    
    Args:
        template_shortid: Shortid du template JSReport (ex: "S1xK9Abc")
        data: Données à injecter dans le template
        options: Options supplémentaires pour JSReport
        
    Returns:
        bytes: Contenu du PDF généré ou None en cas d'erreur
    """
    try:
        # Préparer le payload avec shortid
        payload = {
            "template": {
                "shortid": template_shortid
            },
            "data": data
        }
        
        # Ajouter les options si fournies
        if options:
            payload["options"] = options
            
        # Préparer les headers
        headers = self._get_auth_headers()
        
        logger.info(f"Génération PDF avec shortid: {template_shortid}")
        
        # Appel à JSReport
        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        
        logger.info(f"PDF généré avec succès. Taille: {len(response.content)} bytes")
        return response.content
        
    except Exception as e:
        logger.error(f"Erreur génération PDF (shortid: {template_shortid}): {str(e)}")
        return None

# Utilisation dans vos vues:
# Au lieu de:
# jsreport_service.generate_pdf("Facture_paiement_client", data)
# 
# Utilisez:
# jsreport_service.generate_pdf_by_shortid("SHORTID_ICI", data)
'''
    
    print(updated_service)

if __name__ == "__main__":
    print("🚀 RÉCUPÉRATION DES SHORTIDS JSREPORT")
    print("=" * 60)
    
    templates = get_jsreport_templates()
    
    if templates:
        generate_updated_service()
        
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. ✅ Copiez les shortids affichés ci-dessus")
        print("2. ✅ Modifiez vos vues Django pour utiliser les shortids")
        print("3. ✅ Redéployez JSReport avec la config corrigée")
        print("4. ✅ Testez l'impression avec les shortids")
        
    else:
        print("\n❌ Impossible de récupérer les templates")
        print("Vérifiez que JSReport Railway est accessible et que les templates sont importés")
    
    print("\n📚 Documentation:")
    print("   • Les shortids sont stables et recommandés par JSReport")
    print("   • Plus fiables que les noms de templates")
    print("   • Insensibles à la casse et aux espaces")