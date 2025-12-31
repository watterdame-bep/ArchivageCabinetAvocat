# Guide de Déploiement Railway - Configuration Simple

## Architecture
- **Backend Django** : Service principal sur Railway
- **Base de données** : MySQL service sur Railway  
- **JSReport** : Service séparé sur Railway pour l'impression des rapports

## Étapes de Déploiement

### 1. Préparer le projet
```bash
# Vérifier que collectstatic fonctionne
python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_production
```

### 2. Créer les services sur Railway

#### Service 1: MySQL Database
1. Créer un nouveau service MySQL
2. Railway génère automatiquement les variables : `MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE`, `MYSQLPORT`

#### Service 2: JSReport Service  
1. Déployer JSReport comme service séparé
2. Noter l'URL du service JSReport
3. Configurer les templates JSReport (voir dossier `templates_jsreport/`)

#### Service 3: Django Backend
1. Connecter le repository GitHub
2. Railway détecte automatiquement `railway.json` et `nixpacks.toml`

### 3. Variables d'environnement Django
Ajouter dans le service Django :
```
SECRET_KEY=your-secret-key-here
JSREPORT_SERVICE_URL=https://your-jsreport-service.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=your-jsreport-password
```

### 4. Déploiement
```bash
railway login
railway link
railway up
```

## Configuration JSReport
Les templates JSReport sont dans le dossier `templates_jsreport/`. Utilisez les scripts :
- `scripts/upload_jsreport_templates.py` : Upload des templates
- `scripts/test_jsreport_connection.py` : Test de connexion

## Fichiers de Configuration
- `railway.json` : Configuration Railway
- `nixpacks.toml` : Configuration build
- `settings_production.py` : Settings Django production
- `requirements.txt` : Dépendances Python

## Points Importants
✅ **WhiteNoise** : Gère les fichiers statiques automatiquement  
✅ **MySQL** : Variables générées automatiquement par Railway  
✅ **JSReport** : Service séparé pour l'impression  
✅ **Configuration simple** : Pas de scripts complexes  

## Vérification
Après déploiement, vérifier :
1. Site accessible
2. CSS chargé correctement  
3. Connexion base de données
4. Impression JSReport fonctionnelle