# Guide de Résolution des Problèmes Railway

## Problème: "pip: command not found" lors du build

### Cause
Railway essaie d'utiliser Docker au lieu de Nixpacks, ou il y a un conflit de configuration.

### Solutions

#### 1. Forcer l'utilisation de Nixpacks
Dans `railway.json`, s'assurer que :
```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

#### 2. Vérifier les fichiers de configuration
- ✅ `railway.json` : Configuration Railway
- ✅ `nixpacks.toml` : Configuration Nixpacks  
- ✅ `Procfile` : Commande de démarrage
- ✅ `runtime.txt` : Version Python
- ✅ `.railwayignore` : Fichiers à ignorer

#### 3. Nettoyer et redéployer
```bash
# Supprimer le service Railway existant
# Créer un nouveau service
# Reconnecter le repository
railway login
railway link
railway up
```

#### 4. Variables d'environnement essentielles
```
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=your-secret-key
```

## Problème: Fichiers statiques 404

### Solutions
1. Vérifier que `STATICFILES_DIRS` inclut le dossier `static/`
2. S'assurer que WhiteNoise est configuré correctement
3. Tester `collectstatic` localement

## Problème: Base de données MySQL

### Solutions
1. Créer un service MySQL sur Railway
2. Les variables sont générées automatiquement
3. Pas besoin de configuration manuelle

## Problème: JSReport non accessible

### Solutions
1. Déployer JSReport comme service séparé
2. Configurer `JSREPORT_SERVICE_URL`
3. Uploader les templates avec les scripts fournis

## Test Local
```bash
python test_deployment.py
python test_railway_build.py
```

## Commandes de Debug Railway
```bash
railway logs
railway status
railway variables
```