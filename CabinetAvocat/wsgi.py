"""
WSGI config for CabinetAvocat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Utiliser les settings de production si déployé sur Railway
# Railway définit automatiquement ces variables d'environnement
if os.environ.get('RAILWAY_STATIC_URL') or os.environ.get('RAILWAY_GIT_COMMIT_SHA') or os.environ.get('PORT'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')

application = get_wsgi_application()
