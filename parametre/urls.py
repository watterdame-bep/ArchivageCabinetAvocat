from django.urls import path
from . import views

urlpatterns = [
    path('communes/', views.liste_communes, name='param_communes'),
    path('communes/ajouter/', views.ajouter_commune_ajax, name='ajouter_commune_ajax'),
    path('communes/modifier/<int:id>/', views.modifier_commune_ajax, name='modifier_commune_ajax'),
    path('communes/supprimer/<int:id>/', views.supprimer_commune_ajax, name='supprimer_commune_ajax'),

    path('secteurs/', views.liste_secteurs_ajax, name='param_secteurs'),
    path('secteurs/ajouter/', views.ajouter_secteur_ajax, name='ajouter_secteur'),
    path('secteurs/modifier/<int:secteur_id>/', views.modifier_secteur_ajax, name='modifier_secteur_ajax'),
    path('secteurs/supprimer/<int:secteur_id>/', views.supprimer_secteur_ajax, name='supprimer_secteur_ajax'),
    path('secteurs/retirer_secteur/<int:secteur_id>/<int:commune_id>/', views.supprimer_secteur_ajax, name='retirer_commune_ajax'),

    path('types-dossier/', views.liste_type_dossier_ajax, name='liste_type_dossier'),
    path('types-dossier/ajouter/', views.ajouter_type_dossier_ajax, name='ajouter_type_dossier'),
    path('types-dossier/modifier/<int:type_id>/', views.modifier_type_dossier_ajax, name='modifier_type_dossier_ajax'),
    path('types-dossier/supprimer/<int:type_id>/', views.supprimer_type_dossier_ajax, name='supprimer_type_dossier_ajax'),

    path('parametres/activites/', views.liste_activites_ajax, name='activites_liste'),
    path('parametres/activites/ajouter/', views.ajouter_activite_ajax, name='ajouter_activite'),
    path('parametres/activites/modifier/<int:id>/', views.modifier_activite_ajax, name='modifier_activite_ajax'),
    path('parametres/activites/supprimer/<int:id>/', views.supprimer_activite_ajax, name='supprimer_activite_ajax'),
    

    
    path('specialites/liste/', views.liste_specialites_ajax, name='liste_specialites_ajax'),
    path('specialites/ajouter/', views.ajouter_specialite_ajax, name='ajouter_specialite_ajax'),
    path('specialites/modifier/<int:id>/', views.modifier_specialite_ajax, name='modifier_specialite_ajax'),
    path('specialites/supprimer/<int:id>/', views.supprimer_specialite_ajax, name='supprimer_specialite_ajax'),


    path('tarifs/', views.liste_tarifs_ajax, name='liste_tarifs_ajax'),
    path('tarifs/ajouter/', views.ajouter_tarif_ajax, name='ajouter_tarif_ajax'),
    path('tarifs/modifier/<int:tarif_id>/', views.modifier_tarif_ajax, name='modifier_tarif_ajax'),
    path('tarifs/supprimer/<int:tarif_id>/', views.supprimer_tarif_ajax, name='supprimer_tarif_ajax'),
    path('tarif/<int:tarif_id>/activites/', views.get_activites_tarif, name='get_activites_tarif'),
    path('activites/disponibles/', views.get_activites_disponibles, name='get_activites_disponibles'),


    path('poste/ajouter/', views.ajouter_poste_avocat_ajax, name='ajouter_poste_avocat_ajax'),
    path('poste/<int:id>/modifier/', views.modifier_poste_avocat_ajax, name='modifier_poste_avocat_ajax'),
    path('poste/<int:id>/supprimer/', views.supprimer_poste_avocat_ajax, name='supprimer_poste_avocat_ajax'),

    path('service/ajouter/', views.ajouter_service_cabinet_ajax, name='ajouter_service_cabinet_ajax'),
    path('service/<int:id>/modifier/', views.modifier_service_cabinet_ajax, name='modifier_service_cabinet_ajax'),
    path('service/<int:id>/supprimer/', views.supprimer_service_cabinet_ajax, name='supprimer_service_cabinet_ajax'),


    path('ville/ajouter/', views.ajouter_ville_ajax, name='ajouter_ville_ajax'),
    path('ville/<int:id>/modifier/', views.modifier_ville_ajax, name='modifier_ville_ajax'),
    path('ville/<int:id>/supprimer/', views.supprimer_ville_ajax, name='supprimer_ville_ajax'),


 
    path('juridictions/ajouter/', views.ajouter_juridiction_ajax, name='ajouter_juridiction_ajax'),
    path('juridictions/modifier/<int:id>/', views.modifier_juridiction_ajax, name='modifier_juridiction_ajax'),
    path('juridictions/supprimer/<int:id>/', views.supprimer_juridiction_ajax, name='supprimer_juridiction_ajax'),

    path('types-pieces/ajouter/', views.ajouter_type_piece_ajax, name='ajouter_type_piece_ajax'),
    path('types-pieces/modifier/<int:id>/', views.modifier_type_piece_ajax, name='modifier_type_piece_ajax'),
    path('types-pieces/supprimer/<int:id>/', views.supprimer_type_piece_ajax, name='supprimer_type_piece_ajax'),
    
    path('ajouter-taux/', views.ajouter_taux_ajax, name='ajouter_taux_ajax'),
    path("supprimer-taux/<int:id>/", views.supprimer_taux_ajax, name="supprimer_taux_ajax"),
    
    path('ajouter-banque/', views.ajouter_banque_ajax, name='ajouter_banque_ajax'),
    path("supprimer-banque/<int:id>/", views.supprimer_banque_ajax, name="supprimer_banque_ajax")


   ]
