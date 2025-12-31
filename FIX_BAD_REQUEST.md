# Résolution du Problème "Bad Request (400)" sur Railway

## ✅ Déploiement Réussi !
Gunicorn démarre correctement, le problème n'est plus le build mais la configuration Django.

## 🔍 Diagnostic du Problème

### Cause Principale
L'erreur "Bad Request (400)" est causée par `ALLOWED_HOSTS` qui ne reconnaît pas le domaine Railway.

### Test de Diagnostic
Accéder à : `https://your-app.railway.app/railway-debug/`

Cet endpoint affiche :
- Host actuel
- ALLOWED_HOSTS configurés
- Variables d'environnement Railway
- Configuration Django

## 🛠️ Solutions Appliquées

### 1. ALLOWED_HOSTS Corrigé
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',      # Tous les sous-domaines
    '.up.railway.app',   # Tous les sous-domaines
]

# Ajout automatique du domaine Railway
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)

# Temporaire pour debug
if os.environ.get('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS.append('*')
```

### 2. CSRF_TRUSTED_ORIGINS Corrigé
```python
CSRF_TRUSTED_ORIGINS = [
    'https://.railway.app',
    'https://.up.railway.app',
]
```

## 🚀 Variables d'Environnement Railway

### Variables Automatiques (Railway les génère)
- `RAILWAY_ENVIRONMENT`
- `RAILWAY_PUBLIC_DOMAIN`
- `MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, etc.

### Variables à Ajouter Manuellement
```
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=your-secret-key-here
JSREPORT_SERVICE_URL=https://your-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=your-password
```

## 🔧 Étapes de Résolution

### 1. Vérifier les Variables
Dans Railway Dashboard → Variables :
- Ajouter `SECRET_KEY` si manquant
- Vérifier `DJANGO_SETTINGS_MODULE`

### 2. Tester l'Endpoint de Debug
```
https://your-app.railway.app/railway-debug/
```

### 3. Si le Problème Persiste
Temporairement, ajouter dans Railway Variables :
```
RAILWAY_DEBUG_HOSTS=*
```

Puis dans `settings_production.py` :
```python
if os.environ.get('RAILWAY_DEBUG_HOSTS'):
    ALLOWED_HOSTS = ['*']
```

## ✅ Vérification Finale

Une fois corrigé, vous devriez voir :
1. ✅ Page d'accueil accessible
2. ✅ CSS chargé correctement
3. ✅ Pas d'erreurs 400
4. ✅ Endpoint debug fonctionne

## 🎯 Prochaines Étapes

1. **Tester l'application** : Navigation, connexion
2. **Configurer JSReport** : Service séparé
3. **Uploader templates** : Scripts dans `templates_jsreport/`
4. **Tests d'impression** : Vérifier les rapports PDF