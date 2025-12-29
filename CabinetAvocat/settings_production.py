"""
Configuration Django pour la production sur Railway
"""
import os
from .settings import *

# Mode production
DEBUG = False

# Hosts autorisés
ALLOWED_HOSTS = [
    '.railway.app',
    '.up.railway.app',
    'localhost',
    '127.0.0.1',
]

# CSRF pour Railway
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

# Base de données Railway
MYSQLHOST = os.environ.get('MYSQLHOST')
MYSQLDATABASE = os.environ.get('MYSQLDATABASE')
MYSQLUSER = os.environ.get('MYSQLUSER')
MYSQLPASSWORD = os.environ.get('MYSQLPASSWORD')
MYSQLPORT = int(os.environ.get('MYSQLPORT', 3306))

if MYSQLHOST:
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

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuration Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# JSReport
JSREPORT_URL = os.environ.get('JSREPORT_URL', 'https://votre-jsreport-service.railway.app')
JSREPORT_USERNAME = os.environ.get('JSREPORT_USERNAME', 'admin')
JSREPORT_PASSWORD = os.environ.get('JSREPORT_PASSWORD', '')
JSREPORT_TIMEOUT = int(os.environ.get('JSREPORT_TIMEOUT', '120'))