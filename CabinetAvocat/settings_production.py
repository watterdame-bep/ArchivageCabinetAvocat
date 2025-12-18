import os
from .settings import *

# Configuration pour la production
DEBUG = False

# Hosts autorisés - Railway fournira automatiquement le domaine
ALLOWED_HOSTS = [
    '.railway.app',
    '.up.railway.app',
    'localhost',
    '127.0.0.1',
]

# Configuration PyMySQL pour Railway
import pymysql
pymysql.install_as_MySQLdb()

# Configuration de la base de données pour Railway
# Railway fournira automatiquement les variables d'environnement pour MySQL
# IMPORTANT: Validation stricte - pas de fallback vers localhost

# Récupérer les variables MySQL de Railway avec validation stricte
# ⚠️ Utilisation de os.environ[] au lieu de get() pour forcer l'erreur si manquante
# settings_production.py

DEBUG = False
pymysql.install_as_MySQLdb()

try:
    mysql_host = os.environ['MYSQLHOST']
    mysql_database = os.environ['MYSQLDATABASE']
    mysql_user = os.environ['MYSQLUSER']
    mysql_password = os.environ['MYSQLPASSWORD']
    mysql_port = os.environ.get('MYSQLPORT', '3306')

    print(
        f"🔗 Connexion MySQL Railway: "
        f"{mysql_user}@{mysql_host}:{mysql_port}/{mysql_database}"
    )

except KeyError as e:
    raise RuntimeError(f"❌ Variable Railway MySQL manquante: {e}")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': mysql_database,
        'USER': mysql_user,
        'PASSWORD': mysql_password,
        'HOST': mysql_host,
        'PORT': mysql_port,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}






# Configuration des fichiers statiques pour la production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration des médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Sécurité pour la production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration des sessions
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configuration JSReport pour la production
JSREPORT_URL = os.environ.get('JSREPORT_URL', 'https://your-jsreport-service.railway.app')
JSREPORT_USERNAME = os.environ.get('JSREPORT_USERNAME', 'admin')
JSREPORT_PASSWORD = os.environ.get('JSREPORT_PASSWORD')  # Obligatoire en production
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '120'))  # Plus long en production

# Configuration des logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/tmp/django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'utils.jsreport_service': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'rapport': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'paiement': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configuration de cache pour améliorer les performances
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Configuration de session pour la production
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'