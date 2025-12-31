#!/bin/bash
# Script de déploiement simple pour Railway - Approche YouTube Tutorial

echo "🚀 Déploiement Cabinet Avocat sur Railway - Approche Simple"

# Nettoyer les anciens fichiers statiques
echo "🧹 Nettoyage des anciens fichiers statiques..."
rm -rf staticfiles/

# Collecter les fichiers statiques
echo "📁 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_production

# Vérifier que les fichiers critiques sont présents
echo "🔍 Vérification des fichiers critiques..."
if [ -f "staticfiles/assets/vendor_components/bootstrap/dist/css/bootstrap.css" ]; then
    echo "✅ Bootstrap CSS trouvé"
else
    echo "❌ Bootstrap CSS manquant"
    exit 1
fi

if [ -f "staticfiles/css/vendors_css.css" ]; then
    echo "✅ Vendors CSS trouvé"
else
    echo "❌ Vendors CSS manquant"
    exit 1
fi

echo "✅ Prêt pour le déploiement Railway!"
echo "📋 Commandes Railway:"
echo "   railway login"
echo "   railway link"
echo "   railway up"