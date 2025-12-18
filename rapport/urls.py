from django.urls import path
from . import views

urlpatterns = [
    # Interface rapport client
    path('client/', views.rapport_client_interface, name='rapport_client'),
    
    # Génération de rapport (AJAX)
    path('client/generer/', views.generer_rapport_client, name='generer_rapport_client'),
    
    # Impression directe PDF (même approche que les factures)
    path('client/imprimer/<int:client_id>/', views.imprimer_rapport_client, name='imprimer_rapport_client'),
    
    # Téléchargement de rapport
    path('client/telecharger/<int:rapport_id>/', views.telecharger_rapport_client, name='telecharger_rapport_client'),
]