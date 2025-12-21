#!/usr/bin/env python
"""
Diagnostic JSReport spécifique pour Railway - Problème d'impression en ligne
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service

class JSReportRailwayDiagnostic:
    def __init__(self):
        self.jsreport_url = getattr(settings, 'JSREPORT_URL', 'http://localhost:5488')
        self.username = getattr(settings, 'JSREPORT_USERNAME', 'admin')
        self.password = getattr(settings, 'JSREPORT_PASSWORD', 'admin123')
        
    def check_environment_variables(self):
        """Vérifie les variables d'environnement Railway"""
        print("🌍 VARIABLES D'ENVIRONNEMENT RAILWAY")
        print("=" * 50)
        
        env_vars = [
            'JSREPORT_URL',
            'JSREPORT_USERNAME', 
            'JSREPORT_PASSWORD',
            'JSREPORT_TIMEOUT',
            'RAILWAY_ENVIRONMENT',
            'RAILWAY_PROJECT_NAME'
        ]
        
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                if 'PASSWORD' in var:
                    print(f"✅ {var}: {'*' * len(value)}")
                else:
                    print(f"✅ {var}: {value}")
            else:
                print(f"❌ {var}: NON DÉFINIE")
        
        print(f"\n📋 Configuration Django actuelle:")
        print(f"   JSREPORT_URL: {self.jsreport_url}")
        print(f"   JSREPORT_USERNAME: {self.username}")
        print(f"   JSREPORT_PASSWORD: {'*' * len(self.password) if self.password else 'NON DÉFINI'}")
        print()
        
    def test_railway_jsreport_connection(self):
        """Teste la connexion au service JSReport sur Railway"""
        print("🚂 TEST CONNEXION JSREPORT RAILWAY")
        print("=" * 50)
        
        if not self.jsreport_url or self.jsreport_url == 'http://localhost:5488':
            print("❌ JSREPORT_URL pointe vers localhost")
            print("💡 Sur Railway, vous devez configurer l'URL du service JSReport déployé")
            print("   Exemple: https://votre-jsreport-service.railway.app")
            return False
            
        try:
            print(f"🔗 Test de connexion: {self.jsreport_url}")
            
            # Test de ping
            ping_url = f"{self.jsreport_url}/api/ping"
            response = requests.get(ping_url, timeout=30)
            
            if response.status_code == 200:
                print("✅ Service JSReport accessible")
                return True
            else:
                print(f"❌ Service JSReport non accessible (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError as e:
            print("❌ Erreur de connexion au service JSReport")
            print(f"   Détail: {e}")
            print("\n💡 Causes possibles:")
            print("   1. Service JSReport non déployé sur Railway")
            print("   2. URL JSReport incorrecte")
            print("   3. Service JSReport arrêté")
            return False
        except requests.exceptions.Timeout:
            print("❌ Timeout de connexion (>30s)")
            print("💡 Le service JSReport met trop de temps à répondre")
            return False
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return False
        finally:
            print()
            
    def test_jsreport_authentication(self):
        """Teste l'authentification JSReport"""
        print("🔐 TEST AUTHENTIFICATION JSREPORT")
        print("=" * 50)
        
        try:
            templates_url = f"{self.jsreport_url}/odata/templates"
            
            response = requests.get(
                templates_url,
                auth=(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 200:
                templates = response.json().get('value', [])
                print(f"✅ Authentification réussie")
                print(f"   Nombre de templates: {len(templates)}")
                
                # Vérifier les templates requis
                required_templates = [
                    "Facture_paiement_client",
                    "Facture_dossier", 
                    "Extrait_de_compte_client"
                ]
                
                if templates:
                    template_names = [t.get('name', '') for t in templates]
                    print("   📋 Templates trouvés:")
                    for template in templates:
                        name = template.get('name', 'Sans nom')
                        print(f"      - {name}")
                        
                    print("\n   🔍 Vérification templates requis:")
                    for required in required_templates:
                        if required in template_names:
                            print(f"      ✅ {required}")
                        else:
                            print(f"      ❌ {required} MANQUANT")
                else:
                    print("   ⚠️ Aucun template trouvé")
                    print("   💡 Vous devez importer vos templates dans JSReport")
                    
                return True
                
            elif response.status_code == 401:
                print("❌ Erreur d'authentification")
                print("💡 Vérifiez JSREPORT_USERNAME et JSREPORT_PASSWORD")
                return False
            else:
                print(f"❌ Erreur (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur d'authentification: {e}")
            return False
        finally:
            print()
            
    def test_pdf_generation_simple(self):
        """Teste la génération d'un PDF simple"""
        print("📄 TEST GÉNÉRATION PDF SIMPLE")
        print("=" * 50)
        
        try:
            # Données de test minimales
            test_data = {
                "test": True,
                "date": datetime.now().strftime("%d/%m/%Y"),
                "message": "Test Railway JSReport"
            }
            
            print("🔄 Génération PDF de test...")
            
            pdf_content = jsreport_service.generate_pdf(
                template_name="Facture_paiement_client",
                data=test_data
            )
            
            if pdf_content:
                size_kb = len(pdf_content) / 1024
                print(f"✅ PDF généré avec succès")
                print(f"   Taille: {size_kb:.2f} KB")
                return True
            else:
                print("❌ Échec de génération PDF")
                print("💡 Vérifiez les logs Django pour plus de détails")
                return False
                
        except Exception as e:
            print(f"❌ Erreur de génération: {e}")
            return False
        finally:
            print()
            
    def check_railway_logs_instructions(self):
        """Donne les instructions pour vérifier les logs Railway"""
        print("📋 INSTRUCTIONS VÉRIFICATION LOGS")
        print("=" * 50)
        print("Pour diagnostiquer plus en détail:")
        print()
        print("1️⃣ Logs Django (votre app principale):")
        print("   - Allez sur Railway Dashboard")
        print("   - Sélectionnez votre projet Django")
        print("   - Onglet 'Deployments' > 'View Logs'")
        print("   - Cherchez les erreurs JSReport")
        print()
        print("2️⃣ Logs JSReport (si service séparé):")
        print("   - Sélectionnez le service JSReport")
        print("   - Vérifiez qu'il est bien démarré")
        print("   - Regardez les logs d'erreur")
        print()
        print("3️⃣ Variables d'environnement:")
        print("   - Service Django: vérifiez JSREPORT_URL, JSREPORT_USERNAME, JSREPORT_PASSWORD")
        print("   - Service JSReport: vérifiez les variables d'auth")
        print()
        
    def generate_railway_config_guide(self):
        """Génère un guide de configuration Railway"""
        print("📖 GUIDE CONFIGURATION RAILWAY")
        print("=" * 50)
        
        guide_content = """
# Configuration JSReport sur Railway

## Problème identifié
✅ JSReport fonctionne en local
❌ JSReport ne fonctionne pas en ligne (Railway)

## Solution étape par étape

### 1. Vérifier le déploiement JSReport
```bash
# Vérifiez que JSReport est déployé comme service séparé
# URL exemple: https://votre-jsreport-service.railway.app
```

### 2. Variables d'environnement Django (Railway)
Dans votre service Django Railway, ajoutez:
```
JSREPORT_URL=https://votre-jsreport-service.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise123
JSREPORT_TIMEOUT=120
```

### 3. Variables d'environnement JSReport (Railway)
Dans votre service JSReport Railway, ajoutez:
```
NODE_ENV=production
authentication_enabled=true
authentication_admin_username=admin
authentication_admin_password=VotreMotDePasseSecurise123
extensions_authentication_cookieSession_secret=VotreCleSecrete456
```

### 4. Vérification des templates
- Connectez-vous à votre JSReport en ligne
- Importez tous vos templates depuis votre version locale
- Vérifiez que les noms correspondent exactement

### 5. Test de connexion
```python
python manage.py shell
from utils.jsreport_service import jsreport_service
print(jsreport_service.test_connection())
```

## Causes probables du problème
1. ❌ JSREPORT_URL pointe vers localhost au lieu de l'URL Railway
2. ❌ Service JSReport non déployé sur Railway
3. ❌ Erreur d'authentification (username/password)
4. ❌ Templates manquants dans JSReport en ligne
5. ❌ Timeout trop court pour Railway
"""
        
        with open('JSREPORT_RAILWAY_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(guide_content)
            
        print("📁 Guide sauvegardé: JSREPORT_RAILWAY_GUIDE.md")
        print()
        
    def run_railway_diagnostic(self):
        """Lance le diagnostic complet Railway"""
        print("🚂 DIAGNOSTIC JSREPORT RAILWAY")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("Problème: JSReport fonctionne en local mais pas en ligne")
        print()
        
        # Tests
        self.check_environment_variables()
        connection_ok = self.test_railway_jsreport_connection()
        
        if connection_ok:
            auth_ok = self.test_jsreport_authentication()
            if auth_ok:
                self.test_pdf_generation_simple()
        
        self.check_railway_logs_instructions()
        self.generate_railway_config_guide()
        
        print("🏁 DIAGNOSTIC RAILWAY TERMINÉ")
        print("=" * 60)
        print("💡 Prochaines étapes:")
        print("   1. Vérifiez la configuration Railway avec le guide généré")
        print("   2. Consultez les logs Railway pour plus de détails")
        print("   3. Testez la connexion après correction")

if __name__ == "__main__":
    diagnostic = JSReportRailwayDiagnostic()
    diagnostic.run_railway_diagnostic()