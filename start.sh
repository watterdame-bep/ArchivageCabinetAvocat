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

# Exécuter les migrations
echo "📊 Exécution des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur automatiquement pour Railway
echo "👤 Vérification du superutilisateur Railway..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('🔧 Création du superutilisateur admin pour Railway...')
    User.objects.create_superuser('admin', 'admin@cabinet.com', 'Admin123!')
    print('✅ Superutilisateur créé: admin / Admin123!')
    print('⚠️ Changez le mot de passe après la première connexion!')
else:
    admin_user = User.objects.filter(is_superuser=True).first()
    print(f'✅ Superutilisateur existant: {admin_user.username}')
"

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