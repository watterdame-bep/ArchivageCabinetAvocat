"""
Configuration Django pour Railway
"""
from .settings import *
import os
import pymysql

# Configuration PyMySQL pour remplacer MySQLdb
pymysql.install_as_MySQLdb()

# Fonction pour nettoyer les variables dupliquées
def clean_env_var(var_name, default=''):
    """Nettoyer les variables d'environnement dupliquées"""
    value = os.environ.get(var_name, default)
    
    # Nettoyer les doublons courants
    if var_name == 'MYSQLHOST' and 'mysql.railway.internal' in value:
        # Si dupliqué, prendre seulement la première occurrence
        if value.count('mysql.railway.internal') > 1:
            value = 'mysql.railway.internal'
    
    if var_name == 'MYSQLDATABASE' and 'railway' in value:
        # Si dupliqué, prendre seulement la première occurrence
        if value.count('railway') > 1:
            value = 'railway'
    
    return value

# Configuration pour Railway
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Secret Key depuis les variables d'environnement Railway
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Hosts autorisés pour Railway
ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '*',  # Temporaire pour debug
]

# Configuration de la base de données MySQL Railway avec nettoyage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': clean_env_var('MYSQLDATABASE', 'cabinetavocat'),
        'USER': clean_env_var('MYSQLUSERNAME', 'root'),
        'PASSWORD': clean_env_var('MYSQLPASSWORD', ''),
        'HOST': clean_env_var('MYSQLHOST', 'localhost'),
        'PORT': clean_env_var('MYSQLPORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Configuration des fichiers statiques pour Railway
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ajouter WhiteNoise pour servir les fichiers statiques
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise - Simple et robuste
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Configuration des logs pour Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Sécurité pour Railway (désactivée temporairement pour debug)
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Temporairement désactivé
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True