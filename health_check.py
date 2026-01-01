from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import os

def health_check(request):
    """Vue de health check pour Railway"""
    try:
        # Test de base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"
    
    # Informations système
    health_data = {
        "status": "OK" if db_status == "OK" else "ERROR",
        "database": db_status,
        "debug": settings.DEBUG,
        "django_version": os.environ.get('DJANGO_VERSION', 'Unknown'),
        "python_version": os.environ.get('PYTHON_VERSION', 'Unknown'),
        "environment": {
            "MYSQLHOST": os.environ.get('MYSQLHOST', 'Not set'),
            "MYSQLPORT": os.environ.get('MYSQLPORT', 'Not set'),
            "MYSQLDATABASE": os.environ.get('MYSQLDATABASE', 'Not set'),
            "SECRET_KEY": "Set" if os.environ.get('SECRET_KEY') else "Not set",
        }
    }
    
    status_code = 200 if db_status == "OK" else 500
    return JsonResponse(health_data, status=status_code)