
# Ajouter dans urls.py pour debug Railway
from django.http import JsonResponse
from django.conf import settings
import os

def railway_debug(request):
    """Debug endpoint pour Railway"""
    return JsonResponse({
        'environment': {
            'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT'),
            'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE'),
        },
        'django_settings': {
            'DEBUG': settings.DEBUG,
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': str(settings.STATIC_ROOT),
            'STATICFILES_DIRS': [str(d) for d in settings.STATICFILES_DIRS],
            'STATICFILES_STORAGE': settings.STATICFILES_STORAGE,
        },
        'middleware': settings.MIDDLEWARE,
        'files_test': {
            'staticfiles_exists': os.path.exists(settings.STATIC_ROOT),
            'static_dir_exists': os.path.exists('static'),
        }
    })

# URL: path('railway-debug/', railway_debug, name='railway_debug'),
