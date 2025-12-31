"""
Configuration de production pour Railway
Approche simple et minimaliste
"""

from .settings import *
import os
import pymysql

# Installer PyMySQL comme MySQLdb
pymysql.install_as_MySQLdb()

# Production settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-9nb+f!7lb30p1bxdd4pw+dbq_z7h%zn^8#i_=vpcbvw(-f$sd*')

# Hosts autorisés - Solution robuste pour Railway
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
]

# Ajouter automatiquement le domaine Railway si disponible
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)

# En développement, permettre tous les hosts
if os.environ.get('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS.append('*')  # Temporaire pour debug Railway

# CSRF trusted origins - CORRECTION pour Railway
CSRF_TRUSTED_ORIGINS = [
    'https://.railway.app',
    'https://.up.railway.app',
]

# Ajouter le domaine spécifique si disponible
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
if railway_domain:
    CSRF_TRUSTED_ORIGINS.append(f'https://{railway_domain}')

# Base de données MySQL Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQLDATABASE'),
        'USER': os.environ.get('MYSQLUSER'),
        'PASSWORD': os.environ.get('MYSQLPASSWORD'),
        'HOST': os.environ.get('MYSQLHOST'),
        'PORT': os.environ.get('MYSQLPORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Configuration des fichiers statiques avec WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Ajouter WhiteNoise middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configuration des médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuration JSReport (service séparé sur Railway)
JSREPORT_URL = os.environ.get('JSREPORT_SERVICE_URL', 'http://localhost:5488')
JSREPORT_USERNAME = os.environ.get('JSREPORT_USERNAME', 'admin')
JSREPORT_PASSWORD = os.environ.get('JSREPORT_PASSWORD', '')
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '60000'))

JSREPORT_CONFIG = {
    'url': JSREPORT_URL,
    'username': JSREPORT_USERNAME,
    'password': JSREPORT_PASSWORD,
    'timeout': JSREPORT_TIMEOUT,
    'verify_ssl': True,
    'templates': {
        'rapport_agent': 'rapport_agent',
        'rapport_client': 'rapport_client',
        'rapport_juridiction': 'rapport_juridiction',
        'rapport_commune': 'rapport_commune',
        'rapport_dossier': 'rapport_dossier',
        'rapport_activites_internes': 'rapport_activites_internes',
        'facture_paiement': 'facture_paiement',
        'facture_dossier': 'Facture_dossier',
        'extrait_compte_client': 'Extrait_de_compte_client',
    }
}

# Sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True