# Guide de Déploiement Railway - Cabinet Avocat avec MySQL + JSReport

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   JSReport      │
│   (Django)      │◄──►│   MySQL         │    │   Service       │
│   Railway       │    │   Railway       │    │   Railway       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✅ Prérequis

1. **Service JSReport déjà déployé sur Railway**
   - URL : `https://votre-jsreport.up.railway.app`
   - Credentials configurés
   - Templates créés

2. **Base de données MySQL Railway**
   - Service MySQL ajouté à votre projet
   - URL MySQL disponible

## 🚀 Étapes de Déploiement

### 1. Préparer le Repository Git

```bash
# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Ready for Railway deployment with MySQL + JSReport"

# Ajouter le remote GitHub (si pas encore fait)
git remote add origin https://github.com/votre-username/cabinet-avocat.git

# Pousser vers GitHub
git push -u origin main
```

### 2. Créer le Projet Railway

1. **Nouveau Projet Railway**
   - Aller sur [railway.app](https://railway.app)
   - Créer un nouveau projet
   - Connecter votre repository GitHub

2. **Ajouter le Service MySQL**
   - Dans Railway, cliquer "Add Service"
   - Sélectionner "MySQL"
   - Railway génèrera automatiquement `DATABASE_URL`

### 3. Configuration des Variables d'Environnement

Dans Railway, configurer ces variables **EXACTEMENT** :

```env
# Django Configuration
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-cle-secrete-tres-longue-et-securisee-ici

# MySQL Railway (automatique)
DATABASE_URL=mysql://root:password@tramway.proxy.rlwy.net:51308/railway

# JSReport Service Connection (CRITIQUE)
JSREPORT_SERVICE_URL=https://votre-jsreport-service.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-mot-de-passe-jsreport
JSREPORT_TIMEOUT=60000
JSREPORT_VERIFY_SSL=True

# JSReport Templates
JSREPORT_TEMPLATE_AGENT=rapport_agent
JSREPORT_TEMPLATE_CLIENT=rapport_client
JSREPORT_TEMPLATE_JURIDICTION=rapport_juridiction
JSREPORT_TEMPLATE_COMMUNE=rapport_commune
JSREPORT_TEMPLATE_DOSSIER=rapport_dossier
JSREPORT_TEMPLATE_ACTIVITES=rapport_activites_internes
JSREPORT_TEMPLATE_FACTURE=facture_paiement
```

### 4. Vérification du Déploiement

#### A. Vérifier les Logs Railway
Dans Railway → Deployments → View Logs, vérifier :

```
✅ Installing dependencies...
✅ PyMySQL installed successfully
✅ Collecting static files...
✅ Running migrations...
✅ Starting Gunicorn...
✅ Application started on port 8000
```

#### B. Tester la Connexion MySQL
```bash
# Dans Railway Shell
python manage.py dbshell
# Doit se connecter à MySQL sans erreur
```

#### C. Tester JSReport
```bash
# Dans Railway Shell
python manage.py shell

# Tester la connexion JSReport
from utils.jsreport_service import jsreport_service
print(jsreport_service.test_connection())
# Doit retourner True
```

### 5. Initialisation de la Base de Données

```bash
# Dans Railway Shell
python manage.py migrate
python manage.py createsuperuser
```

## 🔧 Configuration JSReport

### Templates Requis

Votre service JSReport Railway doit contenir ces templates :

| Template | Usage | Données Reçues |
|----------|-------|----------------|
| `rapport_agent` | Rapports des agents | `{agents: [...], cabinet: {...}}` |
| `rapport_client` | Rapports des clients | `{clients: [...], cabinet: {...}}` |
| `rapport_juridiction` | Rapports des juridictions | `{juridictions: [...]}` |
| `rapport_commune` | Rapports des communes | `{communes: [...]}` |
| `rapport_dossier` | Rapports des dossiers | `{dossiers: [...]}` |
| `rapport_activites_internes` | Activités internes | `{activites: [...]}` |
| `facture_paiement` | Factures | `{facture: {...}, paiements: [...]}` |

### Test de Connexion JSReport

```python
# Dans Django Shell Railway
import requests
from requests.auth import HTTPBasicAuth

url = "https://votre-jsreport.up.railway.app/api/report"
auth = HTTPBasicAuth("admin", "votre-password")

# Test simple
response = requests.get(
    "https://votre-jsreport.up.railway.app/api/templates",
    auth=auth
)
print(response.status_code)  # Doit être 200
```

## 🚨 Dépannage

### Erreur MySQL Connection

**Symptôme :** `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")`

**Solutions :**
1. Vérifier que le service MySQL Railway est démarré
2. Vérifier `DATABASE_URL` dans les variables d'environnement
3. Vérifier que `PyMySQL` est installé : `pip list | grep PyMySQL`

### Erreur JSReport Connection

**Symptôme :** `Service JSReport indisponible`

**Solutions :**
1. Vérifier `JSREPORT_SERVICE_URL` (doit être HTTPS)
2. Tester manuellement : `curl https://votre-jsreport.up.railway.app`
3. Vérifier les credentials dans les variables d'environnement
4. Vérifier que le service JSReport Railway est démarré

### Erreur Template JSReport

**Symptôme :** `Template 'rapport_agent' not found`

**Solutions :**
1. Se connecter à JSReport Studio
2. Vérifier que les templates existent
3. Vérifier les noms exacts des templates
4. Vérifier les permissions des templates

### Erreur de Migration

**Symptôme :** `django.db.utils.ProgrammingError: (1146, "Table doesn't exist")`

**Solutions :**
```bash
# Dans Railway Shell
python manage.py migrate --run-syncdb
python manage.py migrate
```

## 📊 Monitoring

### Logs Importants à Surveiller

```bash
# Logs Django
railway logs --filter="django"

# Logs JSReport
railway logs --filter="jsreport"

# Logs MySQL
railway logs --filter="mysql"
```

### Métriques à Surveiller

- **Connexions MySQL** : Nombre de connexions actives
- **Temps de réponse JSReport** : Latence des appels API
- **Erreurs 500** : Erreurs serveur Django
- **Utilisation mémoire** : Consommation RAM

## 🔄 Mise à Jour

```bash
# Faire les modifications
git add .
git commit -m "Description des changements"
git push origin main

# Railway redéploiera automatiquement
# Surveiller les logs pour vérifier le déploiement
```

## 📞 Support Technique

### Commandes de Debug

```bash
# Vérifier la configuration Django
railway run python manage.py check

# Vérifier les migrations
railway run python manage.py showmigrations

# Tester la base de données
railway run python manage.py dbshell

# Tester JSReport
railway run python -c "from utils.jsreport_service import jsreport_service; print(jsreport_service.test_connection())"
```

### URLs de Test

- **Application Django** : `https://votre-app.up.railway.app`
- **Service JSReport** : `https://votre-jsreport.up.railway.app`
- **Admin Django** : `https://votre-app.up.railway.app/admin/`

## ✅ Checklist de Déploiement

- [ ] Service MySQL Railway ajouté
- [ ] Service JSReport Railway fonctionnel
- [ ] Variables d'environnement configurées
- [ ] Repository GitHub connecté
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Test d'impression JSReport réussi
- [ ] Logs sans erreur critique

Votre application Cabinet Avocat est maintenant prête pour la production avec MySQL et JSReport sur Railway ! 🎉