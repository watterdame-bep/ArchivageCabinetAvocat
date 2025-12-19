#!/bin/bash

# Script de démarrage optimisé pour Railway

echo "🚀 Démarrage Cabinet Avocat - Railway Production"

# 1️⃣ Vérifier les variables d'environnement critiques
if [ -z "$MYSQLHOST" ]; then
    echo "❌ Variables MySQL manquantes - Service MySQL non connecté!"
    echo "💡 Connectez le service MySQL au service Django dans Railway Dashboard"
    exit 1
fi

# 2️⃣ Attendre que MySQL soit prêt
echo "⏳ Attente de MySQL Railway..."
python wait_for_mysql.py

if [ $? -ne 0 ]; then
    echo "❌ MySQL Railway non accessible"
    exit 1
fi

echo "✅ MySQL Railway connecté!"

# 3️⃣ Créer toutes les migrations
echo "📝 Création des migrations..."
python manage.py makemigrations --noinput

# 4️⃣ Appliquer toutes les migrations avec syncdb
echo "🔄 Application des migrations..."
python manage.py migrate --noinput --run-syncdb

# 5️⃣ Créer un superutilisateur si nécessaire (protégé)
echo "👤 Création superutilisateur si nécessaire..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@cabinet.com', 'Admin123!')
    print('✅ Superutilisateur créé: admin / Admin123!')
else:
    print('✅ Superutilisateur déjà existant')
" || echo "⚠️ Création superutilisateur ignorée"

# 6️⃣ Collecter les fichiers statiques
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