# Déploiement Railway Ultra-Simple

## Configuration Minimale

### Fichiers Essentiels
- ✅ `Procfile` : Commandes de démarrage
- ✅ `requirements.txt` : Dépendances Python
- ✅ `settings_production.py` : Configuration Django
- ✅ `.env.example` : Variables d'environnement

### Fichiers Supprimés (qui causaient des problèmes)
- ❌ `nixpacks.toml` 
- ❌ `railway.json`
- ❌ `runtime.txt`
- ❌ `build_railway.sh`
- ❌ `railway_simple.json`

## Déploiement

### 1. Créer les Services Railway
1. **MySQL Database** : Créer un service MySQL
2. **JSReport Service** : Déployer JSReport séparément
3. **Django App** : Connecter ce repository

### 2. Variables d'Environnement (Django Service)
```
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=your-secret-key-here
JSREPORT_SERVICE_URL=https://your-jsreport.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=your-password
```

### 3. Déployer
```bash
railway login
railway link
railway up
```

## Architecture
- **Railway détecte automatiquement Python**
- **Nixpacks utilisé par défaut**
- **Procfile définit les commandes**
- **WhiteNoise gère les fichiers statiques**

## Test Local
```bash
python manage.py check --settings=CabinetAvocat.settings_production
python manage.py collectstatic --noinput --settings=CabinetAvocat.settings_production
```

## En cas de problème
1. Supprimer le service Railway
2. Créer un nouveau service
3. Reconnecter le repository
4. Redéployer

Cette approche minimaliste devrait éviter tous les conflits de configuration.