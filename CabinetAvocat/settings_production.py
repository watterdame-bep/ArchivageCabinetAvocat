import os
import sys
from .settings import *

# Production settings
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

# Middleware avec Whitenoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Agent.middleware.ActivityLogMiddleware',
]

# Configuration PyMySQL
import pymysql
pymysql.install_as_MySQLdb()

# Database configuration pour Railway
MYSQLHOST = os.environ.get('MYSQLHOST')
MYSQLDATABASE = os.environ.get('MYSQLDATABASE') 
MYSQLUSER = os.environ.get('MYSQLUSER')
MYSQLPASSWORD = os.environ.get('MYSQLPASSWORD')
MYSQLPORT = int(os.environ.get('MYSQLPORT', 3306))

# Éviter la connexion MySQL pendant collectstatic
COLLECTSTATIC_MODE = 'collectstatic' in ' '.join(sys.argv)

if MYSQLHOST and not COLLECTSTATIC_MODE:
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
            },
        }
    }
else:
    # Utiliser SQLite temporaire pendant collectstatic
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'temp.sqlite3',
        }
    }

# Configuration des fichiers statiques pour Railway
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Pas de STATICFILES_DIRS en production - on utilise seulement les fichiers collectés
STATICFILES_DIRS = []

# Configuration Whitenoise simple
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = False

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# JSReport configuration (service externe)
JSREPORT_URL = os.environ.get('JSREPORT_URL', 'https://votre-jsreport-service.railway.app')
JSREPORT_USERNAME = os.environ.get('JSREPORT_USERNAME', 'admin')
JSREPORT_PASSWORD = os.environ.get('JSREPORT_PASSWORD', '')
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '120'))

# Logging configuration
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
            'level': 'INFO',
            'propagate': False,
        },
    },
}
