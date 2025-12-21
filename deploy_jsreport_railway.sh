#!/bin/bash

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
