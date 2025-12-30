from .settings import *
import os
import dj_database_url
import pymysql
from decouple import config

# Installer PyMySQL comme MySQLdb pour la compatibilité
pymysql.install_as_MySQLdb()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts autorisés pour Railway
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.railway.app',
    '*.up.railway.app',
    config('RAILWAY_PUBLIC_DOMAIN', default=''),
]

# Configuration de la base de données MySQL Railway
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    # Fallback vers la configuration locale MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='cabinet_avocat'),
            'USER': config('DB_USER', default='root'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Configuration des fichiers statiques pour Railway
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuration des médias pour Railway
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Middleware pour les fichiers statiques
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br', 'map']
WHITENOISE_MANIFEST_STRICT = False  # Plus tolérant avec les fichiers manquants

# Configuration JSReport pour Railway (service séparé)
JSREPORT_CONFIG = {
    'url': config('JSREPORT_SERVICE_URL', default='http://localhost:5488'),
    'username': config('JSREPORT_USERNAME', default='admin'),
    'password': config('JSREPORT_PASSWORD', default=''),
    'timeout': 60000,
    'verify_ssl': True,
    'templates': {
        'rapport_agent': config('JSREPORT_TEMPLATE_AGENT', default='rapport_agent'),
        'rapport_client': config('JSREPORT_TEMPLATE_CLIENT', default='rapport_client'),
        'rapport_juridiction': config('JSREPORT_TEMPLATE_JURIDICTION', default='rapport_juridiction'),
        'rapport_commune': config('JSREPORT_TEMPLATE_COMMUNE', default='rapport_commune'),
        'rapport_dossier': config('JSREPORT_TEMPLATE_DOSSIER', default='rapport_dossier'),
        'rapport_activite': config('JSREPORT_TEMPLATE_ACTIVITES', default='rapport_activite'),
        'facture_paiement_client': config('JSREPORT_TEMPLATE_FACTURE', default='Facture_paiement_client'),
        'facture_dossier': config('JSREPORT_TEMPLATE_FACTURE_DOSSIER', default='Facture_dossier'),
        'extrait_compte_client': config('JSREPORT_TEMPLATE_EXTRAIT_COMPTE', default='Extrait_de_compte_client'),
    }
}


# Configuration de sécurité pour la production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration des logs pour Railway
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
        'rapport': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'utils.jsreport_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Configuration des sessions
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Configuration des emails (si nécessaire)
if config('EMAIL_HOST', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cabinetavocat.com')