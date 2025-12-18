# 📤 Export des Templates JSReport Local

## 🎯 Étapes d'Export

### 1. Accéder à JSReport Studio Local
```
http://localhost:5488/studio
```

### 2. Exporter Tous les Templates
1. **Cliquer sur l'icône "Settings"** (⚙️) en haut à droite
2. **Sélectionner "Export"**
3. **Cocher "Include templates"**
4. **Cocher "Include assets"** (si vous avez des images/CSS)
5. **Cliquer "Export"**
6. **Télécharger le fichier .zip**

### 3. Templates à Exporter
Vos templates actuels :
- ✅ `Facture_paiement_client`
- ✅ `Extrait_de_compte_client`
- ✅ `Facture_dossier`
- ✅ `Rapport` (ou `rapport`)

### 4. Structure du Fichier Exporté
```
jsreport-export.zip
├── templates/
│   ├── Facture_paiement_client/
│   │   ├── content.handlebars
│   │   ├── helpers.js
│   │   └── config.json
│   ├── Extrait_de_compte_client/
│   ├── Facture_dossier/
│   └── Rapport/
├── assets/
│   ├── logo.png
│   └── styles.css
└── manifest.json
```

## 📥 Import vers JSReport Production

### 1. Accéder à JSReport Production
```
https://votre-jsreport-service.railway.app/studio
```

### 2. Se Connecter
- **Username** : admin
- **Password** : VotreMotDePasseSecurise

### 3. Importer les Templates
1. **Cliquer sur "Settings"** (⚙️)
2. **Sélectionner "Import"**
3. **Choisir le fichier .zip exporté**
4. **Cliquer "Import"**
5. **Vérifier que tous les templates sont importés**

### 4. Tester les Templates
1. **Ouvrir chaque template**
2. **Cliquer "Preview"** avec des données de test
3. **Vérifier que le PDF se génère correctement**