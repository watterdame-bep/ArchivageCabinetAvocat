# 🚀 Guide de Déploiement Railway - Cabinet Avocat

## 📋 Checklist de Déploiement

### ✅ **Étape 1: Préparation du Code**
- [x] PyMySQL configuré (remplace mysqlclient)
- [x] Settings de production créés
- [x] JSReport service centralisé
- [x] Authentication case-sensitive
- [x] Procfile et scripts de démarrage
- [x] Variables d'environnement configurées

### 🔧 **Étape 2: Configuration Railway**

#### 2.1 Créer le Projet Railway
```bash
# 1. Aller sur https://railway.app
# 2. Se connecter avec GitHub
# 3. Cliquer "New Project"
# 4. Sélectionner "Deploy from GitHub repo"
# 5. Choisir votre repository CabinetAvocat
```

#### 2.2 Ajouter le Service MySQL
```bash
# Dans Railway Dashboard :
# 1. Cliquer "Add Service"
# 2. Sélectionner "Database" → "MySQL"
# 3. Railway créera automatiquement les variables :
#    - MYSQL_HOST
#    - MYSQL_PORT  
#    - MYSQL_DATABASE
#    - MYSQL_USER
#    - MYSQL_PASSWORD
```

#### 2.3 Configurer les Variables d'Environnement
```bash
# Dans Railway Dashboard → Variables :
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-cle-secrete-super-longue-et-complexe
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app

# JSReport (à configurer après déploiement JSReport)
JSREPORT_URL=https://votre-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=VotreMotDePasseSecurise
JSREPORT_TIMEOUT=120
```

### 🐳 **Étape 3: Déployer JSReport**

#### 3.1 Créer un Nouveau Service JSReport
```bash
# Dans Railway Dashboard :
# 1. Cliquer "Add Service"
# 2. Sélectionner "Empty Service"
# 3. Nommer "jsreport-service"
```

#### 3.2 Configurer JSReport
```bash
# Variables JSReport :
NODE_ENV=production
httpPort=$PORT
authentication_admin_username=admin
authentication_admin_password=VotreMotDePasseSecurise
store_provider=fs
```

#### 3.3 Déployer JSReport avec Docker
```dockerfile
# Railway détectera automatiquement le Dockerfile.jsreport
# Ou utiliser le script deploy-jsreport.sh
```

### 📤 **Étape 4: Migration des Templates JSReport**

#### 4.1 Export depuis JSReport Local
```bash
# 1. Démarrer JSReport local
docker run -p 5488:5488 jsreport/jsreport:4.7.0

# 2. Accéder à http://localhost:5488/studio
# 3. Cliquer Settings → Export
# 4. Télécharger jsreport-export.zip
```

#### 4.2 Import vers JSReport Production
```bash
# 1. Accéder à https://votre-jsreport.railway.app/studio
# 2. Se connecter (admin/VotreMotDePasseSecurise)
# 3. Cliquer Settings → Import
# 4. Uploader jsreport-export.zip
```

#### 4.3 Ou Utiliser le Script Automatisé
```bash
python migrate_templates.py
# Suivre les instructions du script
```

### 🧪 **Étape 5: Tests et Validation**

#### 5.1 Test de Déploiement Django
```bash
# Vérifier les logs Railway
railway logs --follow

# Tester l'accès
curl https://votre-app.railway.app
```

#### 5.2 Test de Connexion Base de Données
```bash
# Dans Railway logs, vérifier :
✅ Migrations exécutées
✅ Fichiers statiques collectés
✅ Application démarrée
```

#### 5.3 Test JSReport
```bash
# Tester la génération PDF
python manage.py test_jsreport --verbose
```

## 🎯 **Ordre d'Exécution Recommandé**

### 1️⃣ **Déployer Django d'abord**
```bash
# Push le code sur GitHub
git add .
git commit -m "Ready for Railway deployment"
git push origin main

# Railway déploiera automatiquement
```

### 2️⃣ **Ajouter MySQL**
```bash
# Dans Railway Dashboard
# Add Service → Database → MySQL
```

### 3️⃣ **Configurer les Variables**
```bash
# Ajouter toutes les variables d'environnement
# SAUF les variables JSReport (pas encore déployé)
```

### 4️⃣ **Tester Django**
```bash
# Vérifier que Django fonctionne
# https://votre-app.railway.app/admin
```

### 5️⃣ **Déployer JSReport**
```bash
# Nouveau service Railway pour JSReport
# Utiliser Dockerfile.jsreport
```

### 6️⃣ **Migrer les Templates**
```bash
# Export/Import ou script automatisé
```

### 7️⃣ **Configurer JSReport dans Django**
```bash
# Ajouter les variables JSREPORT_* dans Railway
```

### 8️⃣ **Tests Finaux**
```bash
# Tester la génération de PDF end-to-end
```

## 🚨 **Problèmes Courants et Solutions**

### ❌ **Build Failed - mysqlclient**
```bash
# ✅ RÉSOLU : PyMySQL utilisé à la place
# Vérifier requirements.txt ne contient pas mysqlclient
```

### ❌ **Database Connection Failed**
```bash
# Vérifier que MySQL service est ajouté
# Vérifier les variables MYSQL_* sont auto-générées
```

### ❌ **Static Files Not Found**
```bash
# Vérifier STATIC_ROOT dans settings_production.py
# Vérifier collectstatic dans Procfile
```

### ❌ **JSReport Templates Not Found**
```bash
# Vérifier que les templates sont migrés
# Tester l'accès à JSReport Studio production
```

## ✅ **Validation Finale**

### Checklist de Fonctionnement
- [ ] Django accessible sur Railway
- [ ] Login/logout fonctionne (case-sensitive)
- [ ] Base de données connectée
- [ ] Pages admin accessibles
- [ ] JSReport service déployé
- [ ] Templates JSReport migrés
- [ ] Génération PDF fonctionne
- [ ] Tous les modules testés

### URLs de Test
```bash
# Django App
https://votre-app.railway.app/admin
https://votre-app.railway.app/dossiers
https://votre-app.railway.app/rapport

# JSReport Studio
https://votre-jsreport.railway.app/studio
```

## 🎉 **Résultat Final**

Une fois toutes ces étapes complétées :
- ✅ Application Django déployée sur Railway
- ✅ Base de données MySQL fonctionnelle
- ✅ JSReport service opérationnel
- ✅ Génération PDF en production
- ✅ Tous les templates migrés
- ✅ Application 100% fonctionnelle

**Votre Cabinet Avocat sera entièrement opérationnel en production ! 🚀**