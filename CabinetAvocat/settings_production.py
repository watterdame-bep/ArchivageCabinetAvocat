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

# Configuration CSRF pour Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# Middleware avec WhiteNoise pour servir les fichiers statiques
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajouté pour Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration PyMySQL pour Railway
import pymysql
pymysql.install_as_MySQLdb()

# Configuration de la base de données pour Railway
# ⚠️ IMPORTANT: Railway injecte les variables MySQL AU RUNTIME (pas au build)
# Pendant le build (collectstatic), les variables MySQL ne sont pas encore disponibles

# Variables MySQL Railway (noms utilisés par Railway)
MYSQLHOST = os.environ.get('MYSQLHOST')
MYSQLDATABASE = os.environ.get('MYSQLDATABASE') 
MYSQLUSER = os.environ.get('MYSQLUSER')
MYSQLPASSWORD = os.environ.get('MYSQLPASSWORD')
MYSQLPORT = os.environ.get('MYSQLPORT')

if MYSQLHOST:
    # 🚀 Production (Railway runtime) - Connexion à la base de données existante
    print(f"🔗 Connexion à la base de données existante: {MYSQLUSER}@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}")
    
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
                # Configuration pour MySQL 9.x Railway avec PyMySQL
                'ssl_disabled': True,  # Simplifie la connexion Railway
            },
        }
    }
else:
    # 🔧 Build phase (collectstatic) - MySQL pas encore disponible
    print("⚠️ Variables MySQL non disponibles - Utilisation SQLite temporaire pour le build")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'build_temp.sqlite3',  # DB temporaire pour le build
        }
    }

# Configuration des fichiers statiques pour la production avec WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
            'filename': os.path.join(BASE_DIR, 'django.log'),  # Chemin relatif au projet
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],  # Console seulement pour éviter problèmes de fichier
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