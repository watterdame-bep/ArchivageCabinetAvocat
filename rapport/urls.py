from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal des rapports
    path('', views.rapport_dashboard, name='rapport_dashboard'),
    
    # Interface rapport client
    path('client/', views.rapport_client_interface, name='rapport_client'),
    
    # Interface rapport agent
    path('agent/', views.rapport_agent_interface, name='rapport_agent'),
    
    # Interface rapport juridiction
    path('juridiction/', views.rapport_juridiction_interface, name='rapport_juridiction'),
    
    # Interface rapport commune
    path('commune/', views.rapport_commune_interface, name='rapport_commune'),
    
    # Interface rapport dossier
    path('dossier/', views.rapport_dossier_interface, name='rapport_dossier'),
    path('dossier/imprimer-filtre/', views.imprimer_rapport_dossiers_filtre, name='imprimer_rapport_dossiers_filtre'),
    
    # Génération de rapport (AJAX)
    path('client/generer/', views.generer_rapport_client, name='generer_rapport_client'),
    path('agent/generer/', views.generer_rapport_agent, name='generer_rapport_agent'),
    path('juridiction/generer/', views.generer_rapport_juridiction, name='generer_rapport_juridiction'),
    path('commune/generer/', views.generer_rapport_commune, name='generer_rapport_commune'),
    
    # Impression directe PDF (même approche que les factures)
    path('client/imprimer/<int:client_id>/', views.imprimer_rapport_client, name='imprimer_rapport_client'),
    path('client/imprimer-filtre/', views.imprimer_rapport_clients_filtre, name='imprimer_rapport_clients_filtre'),
    path('agent/imprimer/<int:agent_id>/', views.imprimer_rapport_agent, name='imprimer_rapport_agent'),
    path('agent/imprimer-filtre/', views.imprimer_rapport_agents_filtre, name='imprimer_rapport_agents_filtre'),
    path('juridiction/imprimer/<int:juridiction_id>/', views.imprimer_rapport_juridiction, name='imprimer_rapport_juridiction'),
    path('juridiction/imprimer-filtre/', views.imprimer_rapport_juridictions_filtre, name='imprimer_rapport_juridictions_filtre'),
    path('commune/imprimer/<int:commune_id>/', views.imprimer_rapport_commune, name='imprimer_rapport_commune'),
    path('commune/imprimer-filtre/', views.imprimer_rapport_communes_filtre, name='imprimer_rapport_communes_filtre'),
    
    # Téléchargement de rapport
    path('client/telecharger/<int:rapport_id>/', views.telecharger_rapport_client, name='telecharger_rapport_client'),
    
    # AJAX et fonctionnalités avancées
    path('commune/details/<int:commune_id>/', views.details_commune_ajax, name='details_commune_ajax'),
    path('commune/export-selection/', views.export_communes_selection, name='export_communes_selection'),
    path('commune/export-global/', views.export_communes_global, name='export_communes_global'),
    path('commune/statistiques/', views.statistiques_communes, name='statistiques_communes'),
    
    # Rapports d'activités des dossiers
    path('dossier/activites/<int:dossier_id>/', views.rapport_activites_dossier, name='rapport_activites_dossier'),
    path('dossier/activites-ajax/<int:dossier_id>/', views.activites_dossier_ajax, name='activites_dossier_ajax'),
    path('dossier/statistiques-activites/', views.statistiques_activites_dossiers, name='statistiques_activites_dossiers'),
    
    # Rapports d'activités internes (Structure.Activite)
    path('activites-internes/', views.rapport_activites_internes, name='rapport_activites_internes'),
    path('activites-internes/details-ajax/<int:activite_id>/', views.details_activite_interne_ajax, name='details_activite_interne_ajax'),
    path('activites-internes/generer/', views.generer_rapport_activite_interne, name='generer_rapport_activite_interne'),
    path('activites-internes/imprimer-filtre/', views.imprimer_rapport_activites_internes_filtre, name='imprimer_rapport_activites_internes_filtre'),
    
    # Référentiel de la caisse (ServiceCabinet)
    path('referentiel-caisse/', views.referentielle_caisse, name='referentielle_caisse'),
    path('referentiel-caisse/details/<int:service_id>/', views.details_service_cabinet_ajax, name='details_service_cabinet_ajax'),
    path('referentiel-caisse/generer/', views.generer_rapport_referentiel_caisse, name='generer_rapport_referentiel_caisse'),
    
    # Rapport caisse
    path('caisse/', views.rapport_caisse_interface, name='rapport_caisse'),
    path('caisse/generer/', views.generer_rapport_caisse, name='generer_rapport_caisse'),
    
    # Test JSReport
    path('test-jsreport-agent/', views.test_jsreport_agent, name='test_jsreport_agent'),

]