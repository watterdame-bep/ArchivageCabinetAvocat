# Fix JSReport Chrome Timeout sur Railway

## 🔍 Diagnostic des Logs
```
chrome pdf generation timed out
Rendering request 1 finished with error in 61268 ms
```

**Problème** : Chrome n'arrive pas à générer le PDF dans les 60 secondes sur Railway (ressources limitées).

## ✅ Solutions à Appliquer

### 1. Variables d'Environnement JSReport (CRITIQUE)

Dans le service JSReport Railway, ajouter ces variables :

```bash
# Timeout Chrome (3 minutes au lieu de 60s)
JSREPORT_CHROME_TIMEOUT=180000

# Arguments Chrome pour Railway (obligatoire)
JSREPORT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage,--disable-gpu

# Pool Chrome limité (stabilité)
JSREPORT_CHROME_POOL_SIZE=1

# Mode production
NODE_ENV=production

# Timeout global JSReport
JSREPORT_TIMEOUT=300000
```

### 2. Configuration Django (Backend)

Mettre à jour `settings_production.py` :

```python
# Configuration JSReport optimisée pour Railway
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '300000'))  # 5 minutes

JSREPORT_CONFIG = {
    'url': JSREPORT_URL,
    'username': JSREPORT_USERNAME,
    'password': JSREPORT_PASSWORD,
    'timeout': JSREPORT_TIMEOUT,
    'verify_ssl': True,
    'chrome_timeout': 180000,  # 3 minutes pour Chrome
    'templates': {
        # ... templates
    }
}
```

### 3. Optimisation des Templates JSReport

#### ❌ À Éviter dans les Templates HTML
```html
<!-- Ressources externes lentes -->
<link href="https://cdn.bootstrapcdn.com/bootstrap.css">
<img src="https://external-site.com/image.jpg">
<script src="https://code.jquery.com/jquery.js"></script>
```

#### ✅ À Utiliser
```html
<!-- Ressources locales ou inline -->
<style>
/* CSS inline pour éviter les appels externes */
body { font-family: Arial, sans-serif; }
</style>

<!-- Images en base64 ou assets locaux -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...">
```

### 4. Modification du Service JSReport Django

Dans `utils/jsreport_service.py`, ajouter les timeouts :

```python
def generate_pdf_response(self, template_name, data, filename):
    """Génération PDF avec timeouts optimisés pour Railway"""
    
    payload = {
        'template': {'name': template_name},
        'data': data,
        'options': {
            'preview': False,  # CRITIQUE: Pas de preview en prod
            'timeout': 300000,  # 5 minutes
        }
    }
    
    response = requests.post(
        f"{self.config['url']}/api/report",
        json=payload,
        auth=(self.config['username'], self.config['password']),
        timeout=300,  # 5 minutes
        verify=self.config.get('verify_ssl', True)
    )
```

## 🚀 Étapes d'Application

### 1. Configurer JSReport Service
```bash
# Dans Railway Dashboard → JSReport Service → Variables
JSREPORT_CHROME_TIMEOUT=180000
JSREPORT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage,--disable-gpu
JSREPORT_CHROME_POOL_SIZE=1
NODE_ENV=production
JSREPORT_TIMEOUT=300000
```

### 2. Redéployer JSReport
```bash
# Railway redéploie automatiquement après ajout des variables
```

### 3. Mettre à Jour Django Backend
- Modifier `settings_production.py`
- Modifier `utils/jsreport_service.py`
- Redéployer Django

### 4. Tester
```bash
# Tester un rapport simple d'abord
# Vérifier les logs JSReport
```

## 🔧 Configuration JSReport Dockerfile (si nécessaire)

Si tu as un Dockerfile pour JSReport :

```dockerfile
FROM jsreport/jsreport:4.7.0

# Variables d'environnement optimisées Railway
ENV JSREPORT_CHROME_TIMEOUT=180000
ENV JSREPORT_CHROME_ARGS=--no-sandbox,--disable-dev-shm-usage,--disable-gpu
ENV JSREPORT_CHROME_POOL_SIZE=1
ENV NODE_ENV=production

# Configuration JSReport
COPY jsreport.config.json /app/jsreport.config.json

EXPOSE 5488
```

## 📊 Monitoring

### Logs à Surveiller
```bash
# ✅ Succès
Rendering request finished successfully

# ❌ Échec
chrome pdf generation timed out

# ⚠️ Lenteur
Rendering request finished in [temps] ms
```

### Temps Acceptables
- ✅ < 30s : Excellent
- ⚠️ 30-60s : Acceptable
- ❌ > 60s : Problématique

## 🎯 Résultats Attendus

Après application :
1. ✅ Pas de timeout Chrome
2. ✅ PDF générés en < 60s
3. ✅ Logs "finished successfully"
4. ✅ Rapports fonctionnels dans l'app