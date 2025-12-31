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

def test_static_files(request):
    """Endpoint pour tester la disponibilité des fichiers statiques sur Railway"""
    static_root = settings.STATIC_ROOT
    
    test_files = [
        'css/style.css',
        'css/vendors_css.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    ]
    
    results = {}
    for file_path in test_files:
        full_path = os.path.join(static_root, file_path)
        results[file_path] = {
            'exists': os.path.exists(full_path),
            'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0,
            'full_path': full_path
        }
    
    return JsonResponse({
        'static_root': static_root,
        'static_url': settings.STATIC_URL,
        'staticfiles_dirs': settings.STATICFILES_DIRS,
        'debug': settings.DEBUG,
        'files': results,
        'environment': 'Railway' if 'RAILWAY_ENVIRONMENT' in os.environ else 'Local'
    })

def railway_debug(request):
    """Debug endpoint complet pour Railway"""
    return JsonResponse({
        'environment': {
            'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT', 'Not set'),
            'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set'),
            'PORT': os.environ.get('PORT', 'Not set'),
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
            'staticfiles_count': len(list(os.walk(settings.STATIC_ROOT))) if os.path.exists(settings.STATIC_ROOT) else 0,
        },
        'critical_files': {
            'bootstrap_css': os.path.exists(os.path.join(settings.STATIC_ROOT, 'assets/vendor_components/bootstrap/dist/css/bootstrap.css')),
            'select2_css': os.path.exists(os.path.join(settings.STATIC_ROOT, 'assets/vendor_components/select2/dist/css/select2.min.css')),
            'vendors_css': os.path.exists(os.path.join(settings.STATIC_ROOT, 'css/vendors_css.css')),
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-static/', test_static_files, name='test_static'),
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

# 🔥 CRITIQUE: En production Railway, WhiteNoise gère les fichiers statiques
# Ne pas servir les fichiers statiques via Django URLs en production
if settings.DEBUG:
    # Seulement en développement local
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
