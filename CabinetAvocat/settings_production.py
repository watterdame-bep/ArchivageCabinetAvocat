from .settings import *
import os
import dj_database_url
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts autorisés
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
    config('RAILWAY_PUBLIC_DOMAIN', default=''),
]

# Configuration de la base de données pour Railway
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Fallback vers la configuration locale
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='cabinet_avocat'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
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

# Configuration JSReport pour production Railway
JSREPORT_CONFIG = {
    # URL du service JSReport Railway (sera fournie via variable d'environnement)
    'url': config('JSREPORT_SERVICE_URL', default='http://localhost:5488'),
    'username': config('JSREPORT_USERNAME', default=''),
    'password': config('JSREPORT_PASSWORD', default=''),
    'timeout': config('JSREPORT_TIMEOUT', default=60000, cast=int),
    # Configuration spécifique Railway
    'railway_service': True,
    'verify_ssl': config('JSREPORT_VERIFY_SSL', default=True, cast=bool),
    'templates': {
        'rapport_agent': config('JSREPORT_TEMPLATE_AGENT', default='rapport_agent'),
        'rapport_client': config('JSREPORT_TEMPLATE_CLIENT', default='rapport_client'),
        'rapport_juridiction': config('JSREPORT_TEMPLATE_JURIDICTION', default='rapport_juridiction'),
        'rapport_commune': config('JSREPORT_TEMPLATE_COMMUNE', default='rapport_commune'),
        'rapport_dossier': config('JSREPORT_TEMPLATE_DOSSIER', default='rapport_dossier'),
        'rapport_activites_internes': config('JSREPORT_TEMPLATE_ACTIVITES', default='rapport_activites_internes'),
        'facture_paiement': config('JSREPORT_TEMPLATE_FACTURE', default='facture_paiement'),
    }
}

# Configuration de sécurité pour la production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuration CORS si nécessaire
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    config('FRONTEND_URL', default=''),
]

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