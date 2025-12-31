# Fix JSReport URL - Problème de Schéma

## 🔍 Problème Identifié

```
ERROR: Invalid URL 'cabinet-avocat-jsreport-production.up.railway.app/api/report': 
No scheme supplied. Perhaps you meant https://...?
```

**Cause** : La variable d'environnement `JSREPORT_SERVICE_URL` manque le préfixe `https://`

## ✅ Solution Immédiate

### Option 1: Corriger la Variable d'Environnement (Recommandé)

Dans Railway Dashboard → Django Service → Variables :

**❌ Incorrect :**
```
JSREPORT_SERVICE_URL=cabinet-avocat-jsreport-production.up.railway.app
```

**✅ Correct :**
```
JSREPORT_SERVICE_URL=https://cabinet-avocat-jsreport-production.up.railway.app
```

### Option 2: Correction Automatique (Déjà Appliquée)

Le service JSReport a été modifié pour corriger automatiquement l'URL :
- Si pas de schéma → ajoute `https://` pour Railway
- Si localhost → ajoute `http://`

## 🚀 Étapes de Correction

### 1. Mettre à Jour la Variable
```bash
# Dans Railway Dashboard
JSREPORT_SERVICE_URL=https://cabinet-avocat-jsreport-production.up.railway.app
```

### 2. Redéployer Django
Railway redéploie automatiquement après modification des variables.

### 3. Tester
Essayer de générer un rapport PDF depuis l'application.

## 🔍 Vérification

### Logs Attendus (Après Correction)
```
INFO: 🔧 JSReport configuré: https://cabinet-avocat-jsreport-production.up.railway.app
INFO: 🚀 Génération PDF avec template: rapport_activite
INFO: ✅ PDF généré avec succès. Taille: 12345 bytes
```

### Logs d'Erreur (Avant Correction)
```
ERROR: Invalid URL '...': No scheme supplied
```

## 🎯 Test de Validation

### 1. Endpoint de Debug
Accéder à : `https://your-django-app.railway.app/railway-debug/`

Vérifier que `JSREPORT_URL` contient `https://`

### 2. Test de Génération PDF
Essayer de générer un rapport depuis l'interface Django.

## 📋 Variables JSReport Complètes

```bash
# Django Service Variables
JSREPORT_SERVICE_URL=https://cabinet-avocat-jsreport-production.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=your-secure-password
JSREPORT_TIMEOUT=300000

# JSReport Service Variables (dans le service JSReport)
JSREPORT_CHROME_TIMEOUT=180000
JSREPORT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage,--disable-gpu
JSREPORT_CHROME_POOL_SIZE=1
NODE_ENV=production
```

## 🎯 Résultat Attendu

Après correction :
- ✅ Plus d'erreur "Invalid URL"
- ✅ Connexion JSReport réussie
- ✅ Génération PDF fonctionnelle
- ✅ Rapports téléchargeables depuis l'interface

Cette correction simple devrait résoudre immédiatement le problème de connexion JSReport.