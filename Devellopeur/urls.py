from django.urls import path
from . import views
from CabinetAvocat import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path("Dashboard_Dev_Administrator/", views.dashboard_admin, name="Dashboard_Administrator"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
   # Le media