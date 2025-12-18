from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("dossier/<int:dossier_id>/paiements/", views.gestion_paiements, name="gestion_paiements"),
    path('paiements_cabinet/', views.gestion_paiements_cabinet_client, name='gestion_paiements_cabinet'),
    path('paiements/<int:dossier_id>/', views.gestion_paiements_cabinet_client, name='gestion_paiements_dossier'),

    path("facture/paiement/<int:paiement_id>/", views.imprimer_facture_paiement, name="imprimer_facture_paiement"),
    path("Gestion_caisse/", views.gerer_caisse, name="Gerer_caisse"),
    path('caisse/<int:pk>/json/', views.caisse_detail_json, name='caisse_detail_json'),
    path("caisse/<int:id>/edit/", views.caisse_edit, name="caisse_edit"),
    path("caisse/<int:id>/delete/", views.caisse_delete, name="caisse_delete"),
    path("caisse/sortie/", views.ajouter_sortie, name="ajouter_sortie")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media