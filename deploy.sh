#!/bin/bash

# Script de déploiement pour Railway
echo "🚀 Déploiement Cabinet Avocat sur Railway"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis le répertoire racine du projet Django"
    exit 1
fi

# Vérifier que git est initialisé
if [ ! -d ".git" ]; then
    echo "📦 Initialisation du repository Git..."
    git init
fi

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers au repository..."
git add .

# Demander le message de commit
read -p "💬 Message de commit (ou Entrée pour 'Deploy to Railway'): " commit_message
if [ -z "$commit_message" ]; then
    commit_message="Deploy to Railway"
fi

# Commit
echo "💾 Commit des changements..."
git commit -m "$commit_message"

# Vérifier si le remote origin existe
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Configuration du remote GitHub..."
    read -p "📝 URL du repository GitHub (ex: https://github.com/username/cabinet-avocat.git): " github_url
    git remote add origin "$github_url"
fi

# Pousser vers GitHub
echo "⬆️ Push vers GitHub..."
git push -u origin main

echo "✅ Déploiement terminé!"
echo ""
echo "📋 Prochaines étapes sur Railway:"
echo "1. Connecter votre repository GitHub"
echo "2. Configurer les variables d'environnement (voir .env.example)"
echo "3. Ajouter un service PostgreSQL"
echo "4. Vérifier la connexion à votre service JSReport"
echo ""
echo "🔧 Variables d'environnement importantes:"
echo "   - JSREPORT_SERVICE_URL: URL de votre service JSReport Railway"
echo "   - JSREPORT_USERNAME: Nom d'utilisateur JSReport"
echo "   - JSREPORT_PASSWORD: Mot de passe JSReport"
echo ""
echo "📖 Consultez DEPLOYMENT.md pour plus de détails"