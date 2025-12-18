"""
WSGI config for CabinetAvocat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Utiliser les settings de production si la variable d'environnement est définie
if os.environ.get('RAILWAY_ENVIRONMENT'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')

application = get_wsgi_application()
