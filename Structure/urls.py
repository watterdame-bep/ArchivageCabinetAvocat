from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("Creation_du_Cabinet/", views.creer_cabinet, name="Creation_du_Cabinet"),
    path('ajax/cabinet/', views.parametres_cabinet_ajax, name='parametres_cabinet_ajax'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media