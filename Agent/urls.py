from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("Enregistrer_un_nouvel_agent", views.ajouter_agent, name="Enregistrer_un_nouvel_agent"),
    path('agents/details/<int:agent_id>/', views.details_agent, name='agent_details'),
    path('agents/modifier/<int:agent_id>/', views.modifier_agent, name='modifier_agent'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media