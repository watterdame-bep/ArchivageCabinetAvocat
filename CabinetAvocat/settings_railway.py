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
    'archivagecabinetavocat-production.up.railway.app',  # Votre domaine spécifique
    'localhost',
    '127.0.0.1',
    '*',  # Temporaire pour debug
]

# Configuration CSRF pour Railway
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://archivagecabinetavocat-production.up.railway.app',
]

# Configuration des cookies pour Railway
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Configuration des sessions pour Railway
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Configuration de la base de données MySQL Railway avec nettoyage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': clean_env_var('MYSQLDATABASE', 'cabinetavocat'),
        'USER': clean_env_var('MYSQLUSER', 'root'),
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

# Configuration WhiteNoise - Désactiver la compression pour debug
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuration WhiteNoise pour éviter les erreurs
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br', 'map']
WHITENOISE_MAX_AGE = 31536000  # 1 an

# Répertoires de fichiers statiques
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuration des finders pour s'assurer que tous les fichiers sont trouvés
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

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
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Configuration HSTS pour la sécurité
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True