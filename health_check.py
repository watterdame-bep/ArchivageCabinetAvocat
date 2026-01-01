from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.conf import settings
import os

def health_check(request):
    """Vue de health check simplifiée pour Railway"""
    try:
        # Test simple sans base de données d'abord
        if request.GET.get('simple'):
            return JsonResponse({
                "status": "OK",
                "message": "Django is running",
                "debug": settings.DEBUG,
            })
        
        # Test de base de données
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "OK"
        except Exception as e:
            db_status = f"ERROR: {str(e)}"
        
        # Informations système
        health_data = {
            "status": "OK" if db_status == "OK" else "PARTIAL",
            "database": db_status,
            "debug": settings.DEBUG,
            "environment": {
                "MYSQLHOST": "Set" if os.environ.get('MYSQLHOST') else "Not set",
                "MYSQLPORT": os.environ.get('MYSQLPORT', 'Not set'),
                "MYSQLDATABASE": "Set" if os.environ.get('MYSQLDATABASE') else "Not set",
                "SECRET_KEY": "Set" if os.environ.get('SECRET_KEY') else "Not set",
            }
        }
        
        return JsonResponse(health_data)
        
    except Exception as e:
        # En cas d'erreur, retourner une réponse simple
        return HttpResponse(f"Health check error: {str(e)}", status=500)