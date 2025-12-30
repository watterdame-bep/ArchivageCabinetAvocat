# 🚀 Déploiement Rapide Railway - MySQL + JSReport

## Option 1 : Avec settings_production.py (Recommandé)

### Variables Railway à configurer :
```env
DEBUG=False
DJANGO_SETTINGS_MODULE=CabinetAvocat.settings_production
SECRET_KEY=votre-cle-secrete-longue
DATABASE_URL=mysql://root:password@host:port/railway
JSREPORT_SERVICE_URL=https://votre-jsreport.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-password
```

## Option 2 : Avec settings.py existant (Plus Simple)

### Modifier votre settings.py existant :

```python
# Ajouter en haut du fichier
import os
import dj_database_url
import pymysql

# Installer PyMySQL
pymysql.install_as_MySQLdb()

# Modifier DATABASES
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }

# Ajouter pour Railway
ALLOWED_HOSTS = ['*']  # Temporaire pour test
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration JSReport
JSREPORT_CONFIG = {
    'url': os.environ.get('JSREPORT_SERVICE_URL', 'http://localhost:5488'),
    'username': os.environ.get('JSREPORT_USERNAME', 'admin'),
    'password': os.environ.get('JSREPORT_PASSWORD', ''),
}
```

### Variables Railway (Option 2) :
```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-longue
DATABASE_URL=mysql://root:password@host:port/railway
JSREPORT_SERVICE_URL=https://votre-jsreport.up.railway.app
JSREPORT_USERNAME=admin
JSREPORT_PASSWORD=votre-password
```

## 🔧 Étapes Rapides

1. **Pousser vers GitHub**
```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

2. **Railway**
   - Connecter GitHub repo
   - Ajouter service MySQL
   - Configurer variables d'environnement
   - Déployer

3. **Initialiser**
```bash
# Dans Railway Shell
python manage.py migrate
python manage.py createsuperuser
```

## ✅ Test Rapide

- Ouvrir votre app Railway
- Se connecter à l'admin
- Tester l'impression d'un rapport
- Vérifier que le PDF se génère via JSReport

**C'est tout ! Votre app est en ligne avec MySQL + JSReport** 🎉