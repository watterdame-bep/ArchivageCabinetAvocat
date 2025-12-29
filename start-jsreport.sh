#!/bin/bash

# Script de démarrage pour JSReport avec configuration personnalisée

echo "🚀 Démarrage de JSReport..."

# Vérifier si le fichier d'export existe et l'importer
if [ -f "/app/export.jsrexport" ]; then
    echo "📦 Import des templates depuis export.jsrexport..."
    jsreport import --serverUrl=http://localhost:5488 /app/export.jsrexport
fi

# Démarrer JSReport avec la configuration
echo "🔧 Démarrage du serveur JSReport..."
exec jsreport start --config=/app/jsreport.config.json