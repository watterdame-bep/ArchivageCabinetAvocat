#!/usr/bin/env python
"""
Script de configuration JSReport pour Railway
Aide à configurer JSReport pour fonctionner en production
"""
import os
import json

def create_railway_jsreport_config():
    """Crée les fichiers de configuration pour déployer JSReport sur Railway"""
    
    print("🚂 CONFIGURATION JSREPORT RAILWAY")
    print("=" * 50)
    
    # 1. Créer un docker-compose spécifique pour Railway
    railway_compose = """version: '3.8'

services:
  jsreport:
    build:
      context: .
      dockerfile: Dockerfile.jsreport
    ports:
      - "${PORT:-5488}:${PORT:-5488}"
    environment:
      - NODE_ENV=production
      - httpPort=${PORT:-5488}
      - authentication_enabled=true
      - authentication_admin_username=${JSREPORT_USERNAME:-admin}
      - authentication_admin_password=${JSREPORT_PASSWORD:-admin123}
      - extensions_authentication_cookieSession_secret=${JSREPORT_COOKIE_SECRET:-your-secret-key}
      - workers_numberOfWorkers=2
      - workers_timeout=120000
      - store=fs
      - blobStorage=fs
    volumes:
      - jsreport_data:/app/data
    restart: unless-stopped

volumes:
  jsreport_data:
"""
    
    with open('docker-compose.railway.yml', 'w') as f:
        f.write(railway_compose)
    print("✅ Créé: docker-compose.railway.yml")
    
    # 2. Mettre à jour le Dockerfile JSReport pour Railway
    dockerfile_content = """FROM jsreport/jsreport:4.7.0

# Variables d'environnement Railway
ENV NODE_ENV=production
ENV httpPort=${PORT:-5488}

# Configuration de sécurité
ENV trustUserCode=false
ENV allowLocalFilesAccess=false

# Configuration d'authentification
ENV authentication_enabled=true
ENV extensions_authentication_cookieSession_secret=${JSREPORT_COOKIE_SECRET:-default-secret}

# Configuration de performance pour Railway
ENV workers_numberOfWorkers=2
ENV workers_timeout=120000

# Configuration de stockage
ENV store=fs
ENV blobStorage=fs

# Créer les répertoires nécessaires
RUN mkdir -p /app/data /app/logs

# Exposer le port Railway
EXPOSE ${PORT:-5488}

# Healthcheck pour Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:${PORT:-5488}/api/ping || exit 1

# Commande de démarrage
CMD ["node", "server.js"]
"""
    
    with open('Dockerfile.jsreport', 'w') as f:
        f.write(dockerfile_content)
    print("✅ Mis à jour: Dockerfile.jsreport")
    
    # 3. Créer un script de déploiement Railway
    deploy_script = """#!/bin/bash

echo "🚂 Déploiement JSReport sur Railway"
echo "=================================="

echo "📋 Étapes à suivre manuellement:"
echo ""
echo "1. Créer un nouveau projet Railway:"
echo "   - Allez sur https://railway.app"
echo "   - New Project > Empty Project"
echo "   - Nom: cabinet-avocat-jsreport"
echo ""

echo "2. Ajouter le service JSReport:"
echo "   - New Service > GitHub Repo"
echo "   - Sélectionnez votre repository"
echo "   - Dockerfile Path: Dockerfile.jsreport"
echo ""

echo "3. Configurer les variables d'environnement JSReport:"
echo "   JSREPORT_USERNAME=admin"
echo "   JSREPORT_PASSWORD=VotreMotDePasseSecurise123"
echo "   JSREPORT_COOKIE_SECRET=VotreCleSecrete456"
echo "   NODE_ENV=production"
echo ""

echo "4. Déployer et noter l'URL générée"
echo "   Exemple: https://cabinet-avocat-jsreport-production.up.railway.app"
echo ""

echo "5. Configurer votre service Django Railway:"
echo "   JSREPORT_URL=https://votre-jsreport-url.railway.app"
echo "   JSREPORT_USERNAME=admin"
echo "   JSREPORT_PASSWORD=VotreMotDePasseSecurise123"
echo "   JSREPORT_TIMEOUT=120"
echo ""

echo "6. Redéployer votre service Django"
echo ""

echo "✅ Après déploiement, testez avec:"
echo "   python test_jsreport_quick.py"
"""
    
    with open('deploy_jsreport_railway.sh', 'w') as f:
        f.write(deploy_script)
    os.chmod('deploy_jsreport_railway.sh', 0o755)
    print("✅ Créé: deploy_jsreport_railway.sh")
    
    # 4. Créer un fichier de variables d'environnement exemple
    env_example = """# Variables d'environnement pour JSReport Railway

# Service JSReport
JSREPORT_URL=https://votre-jsreport-service.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise123
JSREPORT_TIMEOUT=120

# Pour le service JSReport lui-même
JSREPORT_COOKIE_SECRET=VotreCleSecrete456
NODE_ENV=production
"""
    
    with open('.env.jsreport.example', 'w') as f:
        f.write(env_example)
    print("✅ Créé: .env.jsreport.example")
    
    # 5. Créer un script de test post-déploiement
    test_script = """#!/usr/bin/env python
import os
import sys
import django
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.conf import settings
from utils.jsreport_service import jsreport_service

def test_production_jsreport():
    print("🧪 TEST JSREPORT PRODUCTION")
    print("=" * 40)
    
    url = settings.JSREPORT_URL
    print(f"URL: {url}")
    
    if 'localhost' in url:
        print("❌ URL contient encore localhost!")
        return False
        
    # Test de connexion
    if jsreport_service.test_connection():
        print("✅ Connexion OK")
        
        # Test des templates
        templates = jsreport_service.get_templates()
        if templates:
            print(f"✅ Templates: {len(templates)} trouvés")
            return True
        else:
            print("❌ Aucun template trouvé")
            return False
    else:
        print("❌ Connexion échouée")
        return False

if __name__ == "__main__":
    test_production_jsreport()
"""
    
    with open('test_jsreport_production.py', 'w') as f:
        f.write(test_script)
    print("✅ Créé: test_jsreport_production.py")
    
    print("\n🎯 FICHIERS CRÉÉS POUR RAILWAY:")
    print("   - docker-compose.railway.yml")
    print("   - Dockerfile.jsreport (mis à jour)")
    print("   - deploy_jsreport_railway.sh")
    print("   - .env.jsreport.example")
    print("   - test_jsreport_production.py")
    
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Exécutez: ./deploy_jsreport_railway.sh")
    print("   2. Suivez les instructions pour déployer sur Railway")
    print("   3. Configurez les variables d'environnement")
    print("   4. Testez avec: python test_jsreport_production.py")

def show_railway_instructions():
    """Affiche les instructions détaillées pour Railway"""
    print("\n" + "="*60)
    print("📖 INSTRUCTIONS DÉTAILLÉES RAILWAY")
    print("="*60)
    
    instructions = """
🎯 OBJECTIF: Faire fonctionner JSReport en production Railway

📋 ÉTAPES DÉTAILLÉES:

1️⃣ CRÉER LE SERVICE JSREPORT
   • Allez sur https://railway.app
   • New Project > Empty Project
   • Nom: "cabinet-avocat-jsreport"
   • New Service > GitHub Repo
   • Sélectionnez votre repository
   • Dockerfile Path: Dockerfile.jsreport

2️⃣ CONFIGURER LES VARIABLES JSREPORT
   Dans le service JSReport, ajoutez:
   • JSREPORT_USERNAME=admin
   • JSREPORT_PASSWORD=VotreMotDePasseSecurise123
   • JSREPORT_COOKIE_SECRET=VotreCleSecrete456
   • NODE_ENV=production

3️⃣ DÉPLOYER ET RÉCUPÉRER L'URL
   • Railway va générer une URL comme:
     https://cabinet-avocat-jsreport-production.up.railway.app
   • Testez l'URL: https://votre-url/api/ping

4️⃣ CONFIGURER VOTRE SERVICE DJANGO
   Dans votre service Django Railway, ajoutez:
   • JSREPORT_URL=https://votre-jsreport-url.railway.app
   • JSREPORT_USERNAME=admin
   • JSREPORT_PASSWORD=VotreMotDePasseSecurise123
   • JSREPORT_TIMEOUT=120

5️⃣ IMPORTER VOS TEMPLATES
   • Connectez-vous à votre JSReport en ligne
   • Importez tous vos templates depuis le local
   • Vérifiez les noms: Facture_paiement_client, etc.

6️⃣ TESTER
   • Redéployez votre service Django
   • Testez l'impression des factures
   • Vérifiez les logs en cas d'erreur

🔧 DÉPANNAGE:
   • Logs JSReport: Railway Dashboard > Service JSReport > Logs
   • Logs Django: Railway Dashboard > Service Django > Logs
   • Test manuel: python test_jsreport_production.py
"""
    
    print(instructions)

if __name__ == "__main__":
    create_railway_jsreport_config()
    show_railway_instructions()