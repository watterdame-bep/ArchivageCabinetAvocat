#!/bin/bash
# Script de build Railway pour Cabinet Avocat

echo "🚀 Début du build Railway"

# Activer l'environnement virtuel
source /opt/venv/bin/activate

# Vérifier les variables d'environnement
echo "📊 Variables d'environnement:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"

# Définir les settings de production
export DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production

# Collecter les fichiers statiques avec verbose
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=2

# Vérifier que les fichiers ont été collectés
echo "🔍 Vérification des fichiers collectés:"
ls -la staticfiles/ || echo "❌ Dossier staticfiles non trouvé"
ls -la staticfiles/css/ || echo "❌ Dossier staticfiles/css non trouvé"
ls -la staticfiles/assets/ || echo "❌ Dossier staticfiles/assets non trouvé"

echo "✅ Build Railway terminé"
