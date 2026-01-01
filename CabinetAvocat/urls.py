from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),  # Health check pour Railway
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
