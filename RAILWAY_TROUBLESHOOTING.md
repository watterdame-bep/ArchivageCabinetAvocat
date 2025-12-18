# 🚨 Guide de Résolution - Problèmes Railway

## ❌ **Problème : Erreur mysqlclient**

### 🎯 **Erreur Rencontrée**
```
Exception: Can not find valid pkg-config name.
Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually
```

### ✅ **Solution Appliquée**
1. **Suppression de mysqlclient** des requirements.txt
2. **Utilisation de PyMySQL** (pure Python, pas de compilation)
3. **Configuration PyMySQL** dans settings.py

### 🔧 **Changements Effectués**

#### requirements.txt
```diff
- mysqlclient==2.2.7
+ # mysqlclient remplacé par PyMySQL (pure Python)
```

#### settings.py
```python
# Configuration PyMySQL pour compatibilité Railway
import pymysql
pymysql.install_as_MySQLdb()
```

## 🚀 **Redéploiement sur Railway**

### 1️⃣ **Pousser les Changements**
```bash
git add .
git commit -m "Fix: Remplace mysqlclient par PyMySQL pour Railway"
git push origin main
```

### 2️⃣ **Railway Redéploiera Automatiquement**
- Railway détectera les changements
- Le build devrait maintenant réussir
- PyMySQL ne nécessite pas de compilation

### 3️⃣ **Vérifier le Déploiement**
```bash
# Vérifier les logs Railway
railway logs

# Tester l'application
curl https://votre-app.railway.app
```

## 🔧 **Autres Problèmes Courants Railway**

### ❌ **Problème : Timeout de Build**
**Solution :**
```toml
# nixpacks.toml
[phases.install]
cmds = [
    "pip install --no-cache-dir -r requirements.txt"
]
```

### ❌ **Problème : Variables d'Environnement**
**Solution :**
1. Aller dans Railway Dashboard
2. Sélectionner votre service
3. Onglet "Variables"
4. Ajouter les variables nécessaires

### ❌ **Problème : Base de Données Non Connectée**
**Erreur:** `Connection refused` ou `Can't connect to MySQL server`

**Solution :**
1. Ajouter un service MySQL dans Railway
2. Railway configurera automatiquement les variables :
   - `MYSQL_HOST`
   - `MYSQL_PORT`
   - `MYSQL_DATABASE`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`

**⚠️ IMPORTANT:** La nouvelle configuration `settings_production.py` **refuse** de démarrer si ces variables manquent (pas de fallback vers localhost).

**Diagnostic:**
```bash
# Utiliser le script de diagnostic
python diagnose_railway.py

# Vérifier les variables MySQL
railway variables

# Voir le guide détaillé
# Consulter RAILWAY_DATABASE_FIX.md
```

### ❌ **Problème : Fichiers Statiques**
**Solution :**
```python
# settings_production.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Utiliser WhiteNoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... autres middlewares
]
```

## 📊 **Checklist de Déploiement Railway**

### ✅ **Avant le Déploiement**
- [ ] PyMySQL configuré (pas mysqlclient)
- [ ] requirements.txt sans dépendances système
- [ ] Variables d'environnement définies
- [ ] Base de données MySQL ajoutée
- [ ] Procfile ou nixpacks.toml configuré

### ✅ **Après le Déploiement**
- [ ] Build réussi (pas d'erreur de compilation)
- [ ] Application accessible
- [ ] Base de données connectée
- [ ] Migrations exécutées
- [ ] Fichiers statiques servis

## 🎯 **Variables d'Environnement Requises**

### **Django**
```
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-cle-secrete
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app
```

### **Base de Données (Auto-configurées par Railway)**
```
MYSQL_HOST=containers-us-west-xxx.railway.app
MYSQL_PORT=3306
MYSQL_DATABASE=railway
MYSQL_USER=root
MYSQL_PASSWORD=xxx
```

### **JSReport**
```
JSREPORT_URL=https://votre-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-password
JSREPORT_TIMEOUT=120
```

## 🚨 **En Cas d'Échec Persistant**

### 1️⃣ **Vérifier les Logs**
```bash
railway logs --follow
```

### 2️⃣ **Tester en Local**
```bash
# Utiliser les mêmes settings de production
export DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
python manage.py check
```

### 3️⃣ **Déploiement Minimal**
```python
# Créer settings_minimal.py avec configuration de base
# Tester d'abord sans JSReport ni fonctionnalités avancées
```

## ✅ **Résultat Attendu**

Après correction, le build Railway devrait afficher :
```
✅ Build successful
✅ Deployment successful  
✅ Application running on https://votre-app.railway.app
```

**PyMySQL résout le problème de compilation MySQL sur Railway ! 🎉**