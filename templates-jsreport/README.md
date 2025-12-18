# 📁 Templates JSReport - Intégration Docker

## 🎯 Objectif
Intégrer vos templates JSReport directement dans l'image Docker pour un déploiement automatique.

## 📋 Structure des Dossiers
```
templates-jsreport/
├── README.md
├── Facture_paiement_client/
│   ├── content.handlebars
│   ├── helpers.js
│   └── config.json
├── Extrait_de_compte_client/
│   ├── content.handlebars
│   ├── helpers.js
│   └── config.json
├── Facture_dossier/
│   ├── content.handlebars
│   ├── helpers.js
│   └── config.json
└── Rapport/
    ├── content.handlebars
    ├── helpers.js
    └── config.json
```

## 🔧 Étapes d'Intégration

### 1. Exporter vos Templates Locaux
1. Accédez à JSReport Studio local: `http://localhost:5488/studio`
2. Pour chaque template, cliquez sur "..." → "Export"
3. Sauvegardez les fichiers dans ce dossier

### 2. Modifier le Dockerfile JSReport
```dockerfile
# Copier les templates dans l'image
COPY ./templates-jsreport/ /app/data/templates/
```

### 3. Script d'Initialisation
Créer un script qui importe automatiquement les templates au démarrage.

## 📝 Format des Fichiers

### config.json
```json
{
  "name": "Facture_paiement_client",
  "engine": "handlebars",
  "recipe": "chrome-pdf",
  "chrome": {
    "format": "A4",
    "margin": {
      "top": "1cm",
      "right": "1cm",
      "bottom": "1cm",
      "left": "1cm"
    }
  }
}
```

### content.handlebars
```handlebars
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Facture de Paiement</title>
    <style>
        /* Vos styles CSS */
    </style>
</head>
<body>
    <h1>Facture N° {{dossier.num_facture}}</h1>
    <!-- Votre contenu HTML avec Handlebars -->
</body>
</html>
```

### helpers.js
```javascript
// Fonctions utilitaires Handlebars
function formatDate(date) {
    // Votre logique de formatage
}
```