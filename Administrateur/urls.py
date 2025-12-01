from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("Dashboard_Cabinet_Administrateur/", views.dashboard_admin, name="Dashboard_Cabinet_Administrateur"),
    path("Agent_Liste/", views.agent_interface, name="Agent_Liste"),
    path("Dashboard_Cabinet_Agent_Avocat/", views.dashboard_Avocat, name="Dashboard_Cabinet_Agent_Avocat"),
    path("Client_client/", views.Interface_Client, name="Client_client"),
    path('parametrage/', views.parametrage_view, name='parametrage'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media