# 🚀 Guide de Déploiement Railway - Cabinet d'Avocats

## 📋 Prérequis

1. **Compte Railway** : [railway.app](https://railway.app)
2. **Projet préparé** avec tous les fichiers de configuration
3. **Repository Git** (GitHub, GitLab, etc.)

## 🔧 Configuration Railway

### 1️⃣ Créer un nouveau projet Railway

```bash
# Installer Railway CLI (optionnel)
npm install -g @railway/cli

# Se connecter à Railway
railway login

# Créer un nouveau projet
railway init
```

### 2️⃣ Configuration des services Railway

**Service 1: MySQL Database**
- Déjà créé dans votre projet Railway
- Railway génère automatiquement les variables de connexion

**Service 2: Backend Django**
- Connecter votre repository Git
- Railway détectera automatiquement Django via `requirements.txt`

**Connexion entre services:**
Railway connecte automatiquement vos services via des variables d'environnement internes.

### 2️⃣ Variables d'environnement à configurer

Dans Railway Dashboard → Service Backend → Variables :

```env
# OBLIGATOIRES (à ajouter manuellement)
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production

# Railway fournit automatiquement ces variables depuis le service MySQL:
# MYSQLHOST=mysql.railway.internal
# MYSQLPORT=3306
# MYSQLUSERNAME=root
# MYSQLPASSWORD=generated_password
# MYSQLDATABASE=railway

# OPTIONNELLES
ALLOWED_HOSTS=*.railway.app
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# JSREPORT (si utilisé)
JSREPORT_URL=https://votre-jsreport-instance.railway.app/api/report
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-mot-de-passe-jsreport
```

**Important :** Railway injecte automatiquement les variables MySQL depuis votre service de base de données. Vous n'avez besoin d'ajouter que les variables Django spécifiques.

### 3️⃣ Base de données MySQL

Railway fournit automatiquement ces variables depuis votre service MySQL :
- `MYSQLHOST` : Adresse du serveur MySQL (ex: mysql.railway.internal)
- `MYSQLPORT` : Port MySQL (généralement 3306)
- `MYSQLUSERNAME` : Nom d'utilisateur MySQL
- `MYSQLPASSWORD` : Mot de passe MySQL généré
- `MYSQLDATABASE` : Nom de la base de données

**Connexion entre services Railway :**
- Votre service backend Django se connectera automatiquement au service MySQL
- Railway gère la communication interne entre services
- Les variables sont injectées automatiquement dans le service backend

### 4️⃣ Commandes de déploiement

**Build Command :**
```bash
python manage.py collectstatic --noinput
```

**Start Command :**
```bash
gunicorn CabinetAvocat.wsgi --bind 0.0.0.0:$PORT
```

## 🗄️ Migration des données

### Depuis MySQL local vers MySQL Railway

1. **Exporter les données MySQL locales :**
```bash
# Exporter la structure et les données
mysqldump -u root -p cabinetavocat > backup_local.sql

# Ou avec Django
python manage.py dumpdata --natural-foreign --natural-primary > data.json
```

2. **Importer dans MySQL Railway :**
```bash
# Via Railway CLI avec fichier SQL
railway connect mysql < backup_local.sql

# Ou avec Django fixtures
railway run python manage.py loaddata data.json
```

### Migrations initiales

```bash
# Localement (pour tester)
python manage.py makemigrations
python manage.py migrate

# Sur Railway (automatique au déploiement)
railway run python manage.py migrate
```

## 📁 Fichiers statiques et media

### Fichiers statiques
✅ **Configuré** : WhiteNoise sert automatiquement les fichiers statiques

### Fichiers media (uploads)
⚠️ **Attention** : Railway utilise un système de fichiers éphémère

**Solutions recommandées :**
1. **AWS S3** + django-storages
2. **Cloudinary** pour images
3. **Railway Volumes** (persistant mais limité)

## 🔐 Sécurité

### HTTPS
✅ Railway fournit automatiquement HTTPS avec certificats SSL

### Variables sensibles
✅ Toutes les variables sensibles sont externalisées

### Recommandations
- Utilisez des mots de passe forts
- Activez l'authentification 2FA sur Railway
- Surveillez les logs d'accès

## 📊 Monitoring et logs

### Voir les logs
```bash
# Via CLI
railway logs

# Via Dashboard
Railway → Projet → Deployments → Logs
```

### Métriques
Railway Dashboard → Metrics :
- CPU usage
- Memory usage
- Network traffic
- Response times

## 🚨 Dépannage

### Erreurs communes

**1. Erreur 500 - Internal Server Error**
```bash
# Vérifier les logs
railway logs

# Vérifier les variables d'environnement
railway variables

# Tester localement avec DEBUG=False
DEBUG=False python manage.py runserver
```

**2. Fichiers statiques non trouvés**
```bash
# Forcer la collecte
railway run python manage.py collectstatic --noinput --clear
```

**3. Erreur de base de données**
```bash
# Vérifier la connexion
railway run python manage.py dbshell

# Réappliquer les migrations
railway run python manage.py migrate --run-syncdb
```

### Commandes utiles

```bash
# Shell Django sur Railway
railway run python manage.py shell

# Créer un superutilisateur
railway run python manage.py createsuperuser

# Vérifier la configuration
railway run python manage.py check --deploy

# Tester la connexion MySQL
railway run python railway_mysql_setup.py

# Configuration complète avec test
railway run python railway_mysql_setup.py --setup
```

### Test de connexion MySQL

```bash
# Tester les variables MySQL Railway
railway run python test_mysql_connection.py

# Voir toutes les variables d'environnement
railway variables

# Tester avec le script complet
railway run python railway_mysql_setup.py

# Debug des variables MySQL spécifiquement
railway run bash -c "echo Host: $MYSQLHOST, Port: $MYSQLPORT, User: $MYSQLUSERNAME, DB: $MYSQLDATABASE"
```

## 📈 Optimisations

### Performance
- Utilisez `DEBUG=False` en production
- Configurez un CDN pour les fichiers statiques
- Optimisez les requêtes de base de données

### Coûts
- Surveillez l'utilisation des ressources
- Utilisez le plan approprié selon le trafic
- Optimisez les images et fichiers media

## 🔄 Mise à jour

### Déploiement automatique
Railway redéploie automatiquement à chaque push sur la branche principale.

### Déploiement manuel
```bash
# Via CLI
railway up

# Via Dashboard
Railway → Projet → Deploy
```

## 📞 Support

- **Documentation Railway** : [docs.railway.app](https://docs.railway.app)
- **Discord Railway** : [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues** : Pour les problèmes spécifiques au projet

---

## ✅ Checklist finale

- [ ] Variables d'environnement configurées
- [ ] Base de données PostgreSQL connectée
- [ ] Fichiers statiques collectés
- [ ] Migrations appliquées
- [ ] HTTPS activé
- [ ] Logs vérifiés
- [ ] Tests de fonctionnement effectués
- [ ] Superutilisateur créé
- [ ] Données migrées (si applicable)

🎉 **Votre cabinet d'avocats est maintenant déployé sur Railway !**