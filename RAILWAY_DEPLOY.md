# 🚀 Déploiement Railway avec Dockerfile + PyMySQL

## 📋 Prérequis

1. **Compte Railway** : [railway.app](https://railway.app)
2. **Service MySQL** déjà créé dans Railway
3. **Repository Git** connecté

## 🔧 Configuration Railway

### 1️⃣ Variables d'environnement

Dans Railway Dashboard → Service Backend → Variables :

```env
# OBLIGATOIRE
SECRET_KEY=wt%6(v^8^+w&u+0#m89!f872h!wn1+ze(c+v+@cqdv-xjdaudz
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_railway

# OPTIONNEL (pour créer un admin automatiquement)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cabinet.com
ADMIN_PASSWORD=votre-mot-de-passe-admin
```

### 2️⃣ Variables MySQL automatiques

Railway injecte automatiquement depuis votre service MySQL :
- `MYSQLHOST` (ex: mysql.railway.internal)
- `MYSQLPORT` (ex: 3306)
- `MYSQLUSERNAME` (ex: root)
- `MYSQLPASSWORD` (généré automatiquement)
- `MYSQLDATABASE` (ex: railway)

### 3️⃣ Configuration du service

1. **Connecter votre repository** au service Railway
2. Railway détectera automatiquement le **Dockerfile**
3. Le build utilisera **PyMySQL** (pas de compilation nécessaire)
4. Le déploiement sera automatique

## 🗄️ Initialisation après déploiement

```bash
# Test de la configuration PyMySQL
railway run python test_pymysql_railway.py

# Exécuter l'initialisation (migrations + superuser)
railway run python railway_init.py

# Ou manuellement :
railway run python manage.py migrate --settings=CabinetAvocat.settings_railway
railway run python manage.py createsuperuser --settings=CabinetAvocat.settings_railway
```

## 🔍 Vérification

1. **Accéder à l'application** : `https://votre-app.railway.app`
2. **Health check** : `https://votre-app.railway.app/health/`
3. **Admin Django** : `https://votre-app.railway.app/admin`
4. **Logs** : `railway logs`

### Logs de démarrage attendus :
```
🚀 Démarrage de l'application Cabinet d'Avocats
📦 Collecte des fichiers statiques...
1822 static files copied to '/app/staticfiles', 2918 post-processed.
🌐 Démarrage du serveur Gunicorn sur le port 8080...
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8080 (1)  ← PORT CORRECT
[INFO] Using worker: sync
[INFO] Booting worker with pid: 35
```

**Important** : Le port doit être `8080` ou la valeur de `$PORT`, jamais `8000` !

## 🚨 Dépannage

### Problème de port (CRITIQUE)
Si vous voyez dans les logs :
```
Listening at: http://0.0.0.0:8000
```
❌ **C'est INCORRECT** - Railway ne peut pas accéder à l'app

✅ **Doit être** :
```
Listening at: http://0.0.0.0:8080
```
ou la valeur de `$PORT`

**Solution** : Vérifiez que le script `start.sh` utilise bien `$PORT`

### Test PyMySQL
```bash
# Tester la configuration PyMySQL
railway run python test_pymysql_railway.py
```

### Health Check
```bash
# Tester le health check
curl https://votre-app.railway.app/health/
```

### Erreur de connexion MySQL
```bash
railway logs | grep -i mysql
railway variables | grep MYSQL
```

### Erreur "No module named 'MySQLdb'"
Cette erreur ne devrait plus apparaître avec PyMySQL, mais si c'est le cas :
```bash
railway run python -c "import pymysql; pymysql.install_as_MySQLdb(); print('PyMySQL OK')"
```

### Erreur de migration
```bash
railway run python manage.py showmigrations --settings=CabinetAvocat.settings_railway
railway run python manage.py migrate --fake-initial --settings=CabinetAvocat.settings_railway
```

### Fichiers statiques manquants
```bash
railway run python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_railway
```

## ✅ Checklist

- [ ] Variables d'environnement configurées
- [ ] Service MySQL connecté
- [ ] Repository Git connecté
- [ ] Dockerfile détecté par Railway
- [ ] Build réussi
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Application accessible