from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("enregistrer_nouveau_client/", views.enregistrer_nouveau_client, name="enregistrer_nouveau_client"),
    path('Client/details/<int:client_id>/', views.details_client, name='client_details'),
    path('Client/update/<int:client_id>/', views.profil_client, name='client_details_mise_a_jour'),
    path('client/<int:client_id>/update_photo/', views.update_client_photo, name='update_client_photo'),
    path("Dossier_interfaces/", views.affaires_interface, name="Dossier_interfaces"),
    path('Dossier/details/<int:dossier_id>/', views.details_affaire, name='dossier_details'),
    path('dossier/<int:dossier_id>/ajouter_pieces/', views.ajouter_pieces, name='ajouter_pieces'),
    path('dossier/<int:dossier_id>/assigner_avocats/', views.assigner_avocats_dossier, name='assigner_avocats_dossier'),
    path( 'supprimer-avocat-dossier/<int:avocat_dossier_id>/', views.supprimer_avocat_dossier, name='supprimer_avocat_dossier'),
    path('dossier/<int:dossier_id>/mode-honoraire/', views.definir_mode_honoraire, name='definir_mode_honoraire'),
    path("dossier/<int:dossier_id>/save-prices/", views.enregistrer_prix_forfaitaire, name="modifier_prix_activites"),
    path('dossier/<int:dossier_id>/enregistrer-prix-forfaitaire/',views.enregistrer_prix_forfaitaire, name='enregistrer_prix_forfaitaire'),
    path('pieces_dossier/<int:piece_id>/supprimer-piece_dossier/',views.supprimer_piece, name='supprimer_piece'),
    path('dossier/<int:dossier_id>/declaration/ajouter/', views.ajouter_declaration, name="ajouter_declaration"),
    path("declaration/<int:decl_id>/modifier/", views.modifier_declaration, name="modifier_declaration"),
    path("declaration/<int:decl_id>/supprimer/", views.supprimer_declaration, name="supprimer_declaration"),
    path('dossier/<int:dossier_id>/extrait-compte-date_form/', views.extrait_compte_date_form, name='extrait_compte_date_form'),
    path('dossier/<int:dossier_id>/extrait-compte-preview/', views.extrait_compte_preview, name='extrait_compte_preview'),
    path('dossier/<int:dossier_id>/extrait-paiements/pdf/', views.imprimer_paiements, name='extrait_compte_pdf'),
    path('dossiers/<int:dossier_id>/print/', views.print_facture, name='print_facture'),
    path('dossier/<int:dossier_id>/cloturer/', views.cloturer_dossier, name='cloturer_dossier'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media