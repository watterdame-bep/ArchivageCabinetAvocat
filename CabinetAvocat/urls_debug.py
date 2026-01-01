from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.db import connection
import os

def simple_test(request):
    """Test ultra-simple"""
    return HttpResponse("Django is working on Railway!")

def health_simple(request):
    """Health check ultra-simple"""
    try:
        # Test DB simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = True
    except:
        db_ok = False
    
    return JsonResponse({
        "status": "OK",
        "database": "OK" if db_ok else "ERROR",
        "mysql_vars": {
            "host": os.environ.get('MYSQLHOST', 'Not set'),
            "port": os.environ.get('MYSQLPORT', 'Not set'),
            "user": os.environ.get('MYSQLUSERNAME', 'Not set'),
            "database": os.environ.get('MYSQLDATABASE', 'Not set'),
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', simple_test, name='simple_test'),
    path('health/', health_simple, name='health_simple'),
    path('', simple_test, name='home'),  # Page d'accueil simple
]