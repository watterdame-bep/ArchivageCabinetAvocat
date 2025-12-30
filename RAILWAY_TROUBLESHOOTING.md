# Guide de Dépannage Railway - Cabinet Avocat

## 🚨 Problèmes Résolus

### 1. Erreur UTF-8 Encoding ✅ RÉSOLU
**Erreur**: `stream did not contain valid UTF-8`
**Solution**: Tous les fichiers convertis en UTF-8 avec le script `fix_encoding_issues.py`

### 2. Erreur MySQL mysqlclient ✅ RÉSOLU  
**Erreur**: `Can not find valid pkg-config name` pour mysqlclient
**Solution**: Remplacement de `mysqlclient` par `PyMySQL` (pure Python)

### 3. Erreur JSReport Package ✅ RÉSOLU
**Erreur**: `No matching distribution found for jsreport-python-client==3.0.0`
**Solution**: Suppression du package inexistant, utilisation de `requests` directement

### 4. Erreur collectstatic WhiteNoise ✅ RÉSOLU
**Erreur**: `MissingFileError: materialdesignicons.css.map could not be found`
**Solution**: Suppression des références sourcemap dans 33 fichiers CSS, configuration WhiteNoise optimisée

## 📋 Configuration Railway Actuelle

### Fichiers de Configuration
- ✅ `requirements.txt` - PyMySQL uniquement (pas mysqlclient)
- ✅ `nixpacks.toml` - Configuration Nixpacks optimisée
- ✅ `railway.json` - Configuration Railway simplifiée
- ✅ `Procfile` - Commande de démarrage Gunicorn
- ✅ `.gitattributes` - Prévention problèmes encodage

### Variables d'Environnement Requises

```bash
# Django
DEBUG=False
SECRET_KEY=votre-cle-secrete-longue
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production

# MySQL Railway
DATABASE_URL=mysql://root:password@host:port/railway

# JSReport Service
JSREPORT_SERVICE_URL=https://votre-jsreport.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-mot-de-passe

# Domaine Railway
RAILWAY_PUBLIC_DOMAIN=votre-app.up.railway.app
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
```

## 🔧 Dépannage Étape par Étape

### Si le Build Échoue Encore

1. **Vérifier les logs Railway**
   ```
   Railway Dashboard → Deployments → Voir les logs
   ```

2. **Problèmes courants et solutions**

   **Erreur**: `ModuleNotFoundError: No module named 'MySQLdb'`
   **Solution**: Vérifier que PyMySQL est installé et configuré dans settings_production.py
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

   **Erreur**: `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module`
   **Solution**: Même correction que ci-dessus

   **Erreur**: `ALLOWED_HOSTS` validation
   **Solution**: Configurer la variable RAILWAY_PUBLIC_DOMAIN

3. **Vérifier la configuration MySQL**
   ```python
   # Dans settings_production.py
   DATABASES = {
       'default': dj_database_url.config(
           default=os.environ.get('DATABASE_URL'),
           conn_max_age=600,
       )
   }
   ```

### Si l'Application Démarre mais ne Fonctionne Pas

1. **Vérifier les migrations**
   ```bash
   # Dans Railway Shell
   python manage.py showmigrations
   python manage.py migrate
   ```

2. **Vérifier les fichiers statiques**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Créer un superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Si JSReport ne Fonctionne Pas

1. **Tester la connexion JSReport**
   ```bash
   python scripts/test_jsreport_connection.py
   ```

2. **Uploader les templates**
   ```bash
   python scripts/upload_jsreport_templates.py
   ```

3. **Vérifier les variables JSReport**
   - JSREPORT_SERVICE_URL doit pointer vers votre service JSReport
   - JSREPORT_USERNAME et JSREPORT_PASSWORD doivent être corrects

## 📊 Commandes de Diagnostic

### Vérification Locale
```bash
# Vérifier la configuration
python check_deployment.py

# Tester la connexion JSReport
python scripts/test_jsreport_connection.py

# Vérifier l'encodage
python fix_encoding_issues.py
```

### Vérification Railway
```bash
# Dans Railway Shell
python manage.py check
python manage.py check --deploy
python manage.py showmigrations
```

## 🚀 Processus de Déploiement Recommandé

1. **Vérification locale**
   ```bash
   python check_deployment.py
   ```

2. **Commit et push**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

3. **Configuration Railway**
   - Créer projet depuis GitHub
   - Ajouter service MySQL Railway
   - Configurer variables d'environnement
   - Déployer

4. **Post-déploiement**
   ```bash
   # Dans Railway Shell
   python manage.py migrate
   python manage.py createsuperuser
   
   # Localement
   python scripts/upload_jsreport_templates.py
   ```

## 📞 Support

### Logs à Vérifier
1. **Railway Build Logs** - Erreurs de compilation
2. **Railway Runtime Logs** - Erreurs d'exécution
3. **Django Logs** - Erreurs application
4. **JSReport Logs** - Erreurs génération PDF

### Fichiers de Configuration Critiques
- `requirements.txt` - Dépendances Python
- `settings_production.py` - Configuration Django
- `nixpacks.toml` - Configuration build Railway
- `railway.json` - Configuration déploiement

### Variables d'Environnement Critiques
- `DATABASE_URL` - Connexion MySQL
- `DJANGO_SETTINGS_MODULE` - Settings Django
- `JSREPORT_SERVICE_URL` - Service JSReport
- `SECRET_KEY` - Sécurité Django

## ✅ Checklist Finale

Avant de déployer, vérifier que :
- [ ] Tous les fichiers sont en UTF-8
- [ ] PyMySQL est utilisé (pas mysqlclient)
- [ ] Variables d'environnement configurées
- [ ] Service MySQL Railway créé
- [ ] Service JSReport Railway créé
- [ ] Templates JSReport prêts à uploader
- [ ] Tests locaux passent

Le déploiement devrait maintenant réussir ! 🎉