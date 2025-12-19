#!/bin/bash

# Script de démarrage pour Railway avec attente MySQL

echo "🚀 Démarrage de l'application Cabinet Avocat..."

# Vérifier les variables d'environnement critiques
if [ -z "$MYSQL_HOST" ]; then
    echo "❌ Variable MYSQL_HOST non définie - Service MySQL manquant!"
    exit 1
fi

# Attendre que MySQL soit prêt avec script dédié
echo "⏳ Vérification de MySQL Railway..."
python wait_for_mysql.py

if [ $? -ne 0 ]; then
    echo "❌ Impossible de se connecter à MySQL Railway"
    echo "🔧 Vérifiez que le service MySQL est ajouté dans Railway Dashboard"
    exit 1
fi

echo "✅ MySQL Railway prêt!"

# Setup initial de la base de données Railway
echo "🔧 Setup initial de la base de données..."
python setup_railway_database.py

if [ $? -ne 0 ]; then
    echo "❌ Échec du setup initial"
    exit 1
fi

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Application prête à démarrer!"

# Démarrer l'application avec Gunicorn optimisé pour Railway
exec gunicorn CabinetAvocat.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile -