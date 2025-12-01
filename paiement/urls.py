from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("dossier/<int:dossier_id>/paiements/", views.gestion_paiements, name="gestion_paiements"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media