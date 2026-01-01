"""
Django settings for CabinetAvocat project - PRODUCTION RAILWAY

Configuration optimisée pour le déploiement sur Railway
"""

from pathlib import Path
import os
from decouple import config
import pymysql

# Configuration PyMySQL pour remplacer mysqlclient
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-9nb+f!7lb30p1bxdd4pw+dbq_z7h%zn^8#i_=vpcbvw(-f$sd*')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts autorisés pour Railway
ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '*',  # Temporaire pour debug
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Authentification.apps.AuthentificationConfig',
    'Structure',
    'Agent.apps.AgentConfig',
    'Devellopeur',
    'Adresse',
    'Dossier',
    'django_select2',
    'parametre',
    'django.contrib.humanize',
    'paiement',
    'rapport',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour servir les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'Agent.middleware.ActivityLogMiddleware',  # Temporairement désactivé pour debug
]

ROOT_URLCONF = 'CabinetAvocat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CabinetAvocat.wsgi.application'

# Database - Configuration Railway avec variables individuelles MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQLDATABASE', default='cabinetavocat'),
        'USER': config('MYSQLUSERNAME', default='root'),
        'PASSWORD': config('MYSQLPASSWORD', default=''),
        'HOST': config('MYSQLHOST', default='localhost'),
        'PORT': config('MYSQLPORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
        'CONN_MAX_AGE': 0,  # Désactiver la réutilisation des connexions pour debug
        'CONN_HEALTH_CHECKS': False,  # Désactiver les health checks DB pour debug
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Configuration WhiteNoise pour les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentification personnalisée
AUTH_USER_MODEL = 'Authentification.CompteUtilisateur'
LOGIN_URL = 'Connexion'
AUTHENTICATION_BACKENDS = ['Authentification.backends.Sensible_Case']

# JSReport Configuration pour Railway
JSREPORT_URL = config('JSREPORT_URL', default='http://localhost:5488')
JSREPORT_USERNAME = config('JSREPORT_USERNAME', default='admin')
JSREPORT_PASSWORD = config('JSREPORT_PASSWORD', default='admin123')
JSREPORT_TIMEOUT = config('JSREPORT_TIMEOUT', default=60, cast=int)

# Sécurité pour production (temporairement désactivée pour debug)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging pour production
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
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',  # Réduire le bruit des requêtes SQL
            'propagate': False,
        },
        'CabinetAvocat': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}