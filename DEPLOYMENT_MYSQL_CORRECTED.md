# Déploiement Railway - Configuration MySQL + JSReport

## Architecture du Déploiement

### 1. Service JSReport (Projet séparé)
- **Projet Railway**: `jsreport-service`
- **URL publique**: `https://votre-jsreport-service.up.railway.app`
- **Authentification**: Admin configuré
- **Templates**: Uploadés via script

### 2. Backend Django (Projet principal)
- **Base de données**: MySQL Railway (PAS PostgreSQL)
- **Fichiers statiques**: WhiteNoise
- **Configuration**: Production optimisée

## Configuration Railway

### Variables d'environnement (Backend Django)

```bash
# Django
DEBUG=False
SECRET_KEY=votre-cle-secrete-longue-et-securisee
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production

# MySQL Railway (IMPORTANT: pas PostgreSQL)
DATABASE_URL=mysql://root:password@tramway.proxy.rlwy.net:51308/railway

# Domaine Railway
RAILWAY_PUBLIC_DOMAIN=votre-app.up.railway.app
ALLOWED_HOSTS=*.railway.app,*.up.railway.app

# JSReport Service (service séparé)
JSREPORT_SERVICE_URL=https://votre-jsreport-service.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-mot-de-passe-jsreport
JSREPORT_TIMEOUT=60000
JSREPORT_VERIFY_SSL=True

# Templates JSReport
JSREPORT_TEMPLATE_AGENT=rapport_agent
JSREPORT_TEMPLATE_CLIENT=rapport_client
JSREPORT_TEMPLATE_JURIDICTION=rapport_juridiction
JSREPORT_TEMPLATE_COMMUNE=rapport_commune
JSREPORT_TEMPLATE_DOSSIER=rapport_dossier
JSREPORT_TEMPLATE_ACTIVITES=rapport_activites_internes
JSREPORT_TEMPLATE_FACTURE=facture_paiement
```

## Étapes de Déploiement

### 1. Préparer JSReport Service

```bash
# 1. Créer projet Railway pour JSReport
# 2. Déployer JSReport depuis template Railway
# 3. Configurer authentification admin
# 4. Noter l'URL publique du service
```

### 2. Uploader les Templates JSReport

```bash
# Configurer les variables d'environnement
export JSREPORT_SERVICE_URL="https://votre-jsreport-service.up.railway.app"
export JSREPORT_USERNAME="admin"
export JSREPORT_PASSWORD="votre-mot-de-passe"

# Uploader les templates
python scripts/upload_jsreport_templates.py
```

### 3. Déployer Backend Django

```bash
# 1. Pousser le code sur GitHub
git add .
git commit -m "Préparation déploiement Railway MySQL + JSReport"
git push origin main

# 2. Créer projet Railway depuis GitHub
# 3. Configurer les variables d'environnement (voir ci-dessus)
# 4. Ajouter service MySQL Railway
```

### 4. Configuration Post-Déploiement

```bash
# Dans Railway Shell (backend Django)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Vérification du Déploiement

### 1. Tester JSReport Service
```bash
curl -u admin:password https://votre-jsreport-service.up.railway.app/api/templates
```

### 2. Tester Backend Django
```bash
curl https://votre-app.up.railway.app/admin/
```

### 3. Tester Impression PDF
- Aller sur un rapport (agents, clients, etc.)
- Cliquer sur "Imprimer"
- Vérifier la génération PDF

## Différences avec PostgreSQL

### ❌ Configuration PostgreSQL (INCORRECTE)
```python
# NE PAS UTILISER
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://...'
    )
}
```

### ✅ Configuration MySQL (CORRECTE)
```python
# UTILISER CECI
import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),  # mysql://...
        conn_max_age=600,
    )
}
```

## Fichiers Créés/Modifiés

- ✅ `settings_production.py` - Configuration MySQL + JSReport
- ✅ `requirements.txt` - Dépendances MySQL
- ✅ `railway.json` - Configuration Railway
- ✅ `Procfile` - Commandes de démarrage
- ✅ `runtime.txt` - Version Python
- ✅ `.env.example` - Variables d'environnement
- ✅ `templates_jsreport/` - Templates JSReport
- ✅ `scripts/upload_jsreport_templates.py` - Upload automatique

## Templates JSReport Créés

Tous les templates sont prêts pour être personnalisés:

- `rapport_agent.html` + `rapport_agent.json`
- `rapport_client.html` + `rapport_client.json`
- `rapport_juridiction.html` + `rapport_juridiction.json`
- `rapport_commune.html` + `rapport_commune.json`
- `rapport_dossier.html` + `rapport_dossier.json`
- `rapport_activites_internes.html` + `rapport_activites_internes.json`
- `facture_paiement.html` + `facture_paiement.json`

## Prochaines Étapes

1. **Personnaliser les templates JSReport** - Ajouter votre contenu HTML/CSS
2. **Tester l'upload** - Utiliser le script d'upload
3. **Déployer sur Railway** - Suivre les étapes ci-dessus
4. **Vérifier l'intégration** - Tester l'impression PDF

## Support

En cas de problème:
1. Vérifier les logs Railway
2. Tester la connexion JSReport
3. Vérifier la configuration MySQL
4. Utiliser le script de vérification: `python check_deployment.py`