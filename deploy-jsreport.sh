#!/bin/bash

# Script de déploiement JSReport sur Railway
# Ce script vous guide pour déployer JSReport séparément

echo "🚀 Déploiement JSReport sur Railway"
echo "=================================="

echo "📋 Étapes à suivre :"
echo ""
echo "1. Créer un nouveau projet Railway pour JSReport :"
echo "   - Allez sur https://railway.app"
echo "   - Cliquez sur 'New Project'"
echo "   - Sélectionnez 'Empty Project'"
echo "   - Nommez-le 'cabinet-avocat-jsreport'"
echo ""

echo "2. Ajouter le service JSReport :"
echo "   - Dans votre projet, cliquez sur 'New Service'"
echo "   - Sélectionnez 'GitHub Repo'"
echo "   - Choisissez ce repository"
echo "   - Configurez le service pour utiliser Dockerfile.jsreport"
echo ""

echo "3. Configurer les variables d'environnement :"
echo "   Dans les settings du service JSReport, ajoutez :"
echo "   - JSREPORT_USERNAME=admin"
echo "   - JSREPORT_PASSWORD=VotreMotDePasseSecurise123"
echo "   - JSREPORT_COOKIE_SECRET=VotreCleSecrete456"
echo "   - NODE_ENV=production"
echo ""

echo "4. Déployer et obtenir l'URL :"
echo "   - Railway va automatiquement déployer JSReport"
echo "   - Notez l'URL générée (ex: https://cabinet-avocat-jsreport-production.up.railway.app)"
echo ""

echo "5. Configurer Django pour utiliser JSReport :"
echo "   Dans votre projet Django Railway, ajoutez la variable :"
echo "   - JSREPORT_URL=https://votre-jsreport-url.railway.app"
echo "   - JSREPORT_USERNAME=admin"
echo "   - JSREPORT_PASSWORD=VotreMotDePasseSecurise123"
echo ""

echo "6. Tester la connexion :"
echo "   - Accédez à votre URL JSReport"
echo "   - Connectez-vous avec admin/VotreMotDePasseSecurise123"
echo "   - Importez vos templates existants"
echo ""

echo "✅ Une fois terminé, vos deux services Railway communiqueront :"
echo "   - Django : Votre application principale"
echo "   - JSReport : Service de génération de PDF"
echo ""

echo "🔧 Commandes utiles :"
echo "   # Tester la connexion JSReport depuis Django"
echo "   python manage.py shell -c \"from utils.jsreport_service import test_jsreport_connection; print(test_jsreport_connection())\""
echo ""

echo "📚 Documentation :"
echo "   - Railway : https://docs.railway.app"
echo "   - JSReport : https://jsreport.net/learn"