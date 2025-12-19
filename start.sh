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
echo "� Step 1o: Création des migrations Django..."
python manage.py makemigrations --noinput

# 4️⃣ Appliquer toutes les migrations avec syncdb (FORCE la création des tables)
echo "� AStep 2: Application des migrations avec --run-syncdb..."
python manage.py migrate --noinput --run-syncdb

# 5️⃣ Exécuter le fix définitif si nécessaire (sécurité)
echo "�  Step 3: Vérification et fix des tables manquantes..."
python fix_railway_tables.py || echo "⚠️ Fix tables ignoré (probablement déjà OK)"

# 6️⃣ Créer un superutilisateur si nécessaire (protégé)
echo "🔹 Step 4: Création superutilisateur si nécessaire..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@cabinet.com', 'Admin123!')
    print('✅ Superutilisateur créé: admin / Admin123!')
else:
    print('✅ Superutilisateur déjà existant')
" || echo "⚠️ Création superutilisateur ignorée"

# 7️⃣ Collecter les fichiers statiques
echo "� Step 5t: Collection des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🔹 Step 6: Lancement du serveur Gunicorn..."
echo "✅ Toutes les étapes terminées - Application prête!"

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