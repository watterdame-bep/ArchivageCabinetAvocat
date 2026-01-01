"""
Configuration Django pour Railway
"""
from .settings import *
import os
import pymysql

# Configuration PyMySQL pour remplacer MySQLdb
pymysql.install_as_MySQLdb()

# Configuration pour Railway
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Secret Key depuis les variables d'environnement Railway
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Hosts autorisés pour Railway
ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
]

# Configuration de la base de données MySQL Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQLDATABASE', 'cabinetavocat'),
        'USER': os.environ.get('MYSQLUSERNAME', 'root'),
        'PASSWORD': os.environ.get('MYSQLPASSWORD', ''),
        'HOST': os.environ.get('MYSQLHOST', 'localhost'),
        'PORT': os.environ.get('MYSQLPORT', '3306'),
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
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

# Sécurité pour Railway (HTTPS)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True