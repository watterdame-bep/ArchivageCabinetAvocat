#!/bin/bash
# Script de déploiement Railway pour Cabinet d'Avocats

echo "🚀 Démarrage du déploiement Railway..."

# Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Migrations de la base de données
echo "🗄️ Application des migrations..."
python manage.py migrate

echo "✅ Déploiement terminé avec succès!"