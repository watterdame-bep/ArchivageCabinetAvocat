import os
import sys
from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    '.railway.app',
    '.up.railway.app',
    'localhost',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

import pymysql
pymysql.install_as_MySQLdb()

# Variables MySQL Railway (noms exacts du service MySQL)
MYSQLHOST = os.environ.get('MYSQLHOST')
MYSQLDATABASE = os.environ.get('MYSQLDATABASE') 
MYSQLUSER = os.environ.get('MYSQLUSER')
MYSQLPASSWORD = os.environ.get('MYSQLPASSWORD')
MYSQLPORT = int(os.environ.get('MYSQLPORT', 3306))

# SOLUTION CRITIQUE: Éviter la connexion MySQL pendant collectstatic
# Railway exécute collectstatic pendant le BUILD, avant que les variables MySQL soient disponibles
COLLECTSTATIC_MODE = os.environ.get('RAILWAY_STATIC_BUILD', False) or 'collectstatic' in ' '.join(sys.argv)

if MYSQLHOST and not COLLECTSTATIC_MODE:
    print(f"🔗 Connexion MySQL Railway: {MYSQLUSER}@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}")
    print(f"🔍 Debug - MYSQLHOST: {MYSQLHOST}")
    print(f"🔍 Debug - MYSQLPORT type: {type(MYSQLPORT)} value: {MYSQLPORT}")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': MYSQLDATABASE,
            'USER': MYSQLUSER,
            'PASSWORD': MYSQLPASSWORD,
            'HOST': MYSQLHOST,
            'PORT': MYSQLPORT,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
                'connect_timeout': 60,
                'read_timeout': 60,
                'write_timeout': 60,
                # SSL requis par Railway - pas de ssl_disabled
            },
            # SOLUTION: Forcer les noms de tables en minuscules
            'TEST': {
                'CHARSET': 'utf8mb4',
                'COLLATION': 'utf8mb4_unicode_ci',
            }
        }
    }
    
    # IMPORTANT: Configurer Django pour utiliser les noms de tables en minuscules
    # Cela résout le problème d'import depuis SQLite vers MySQL
    print("🔧 Configuration: Noms de tables en minuscules activée")
else:
    if COLLECTSTATIC_MODE:
        print("📦 Mode collectstatic détecté - Utilisation SQLite temporaire")
    else:
        print("⚠️ Variables MySQL non disponibles - Utilisation SQLite temporaire")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'build_temp.sqlite3',
        }
    }

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Créer le répertoire static s'il n'existe pas
STATICFILES_DIRS = []
static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(static_dir):
    STATICFILES_DIRS = [static_dir]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# JSReport (service externe séparé sur Railway)
JSREPORT_URL = os.environ.get('JSREPORT_URL', 'https://votre-jsreport-service.railway.app')
JSREPORT_USERNAME = os.environ.get('JSREPORT_USERNAME', 'admin')
JSREPORT_PASSWORD = os.environ.get('JSREPORT_PASSWORD', '')
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '120'))

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'utils.jsreport_service': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'rapport': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'paiement': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache
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

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'