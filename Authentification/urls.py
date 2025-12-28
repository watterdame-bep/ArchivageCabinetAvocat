from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("", views.login_view, name="Connexion"),
    path('agents/creer-compte/', views.creer_utilisateur_agent, name='creer_utilisateur_agent'),
    path('get-cabinet-name/', views.get_cabinet_name, name='get_cabinet_name'),
    path('changer-mot-de-passe/', views.change_password, name='change_password'),
    path('mon-profil/', views.user_profile_view, name='user_profile'),
    path('modifier-profil/', views.edit_profile_view, name='edit_profile'),
    path("Connexion/", views.deconnexion, name="Deconnecter"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media