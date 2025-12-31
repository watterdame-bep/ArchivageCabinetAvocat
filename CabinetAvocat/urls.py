"""
URL configuration for CabinetAvocat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def railway_debug(request):
    """Debug endpoint pour Railway"""
    return JsonResponse({
        'status': 'OK',
        'host': request.get_host(),
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'csrf_trusted_origins': settings.CSRF_TRUSTED_ORIGINS,
        'debug': settings.DEBUG,
        'railway_env': os.environ.get('RAILWAY_ENVIRONMENT', 'Not set'),
        'railway_domain': os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'Not set'),
        'static_url': settings.STATIC_URL,
        'database_name': settings.DATABASES['default']['NAME'],
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('railway-debug/', railway_debug, name='railway_debug'),
    path('',include('Authentification.urls')),
    path('',include('Devellopeur.urls')),
    path('',include('Structure.urls')),
    path('',include('Administrateur.urls')),
    path('',include('Agent.urls')),
    path('',include('Dossier.urls')),
    path('select2/', include('django_select2.urls')),
    path('',include('parametre.urls')),
    path('',include('paiement.urls')),
    path('rapport/', include('rapport.urls'))
]

# En développement seulement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
