from django.http import JsonResponse
from django.db import connection
import os

def health_check(request):
    """Health check simple pour Railway"""
    try:
        # Test de base de données simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "OK"
    except Exception as e:
        db_status = f"ERROR: {str(e)}"
    
    return JsonResponse({
        "status": "OK" if db_status == "OK" else "PARTIAL",
        "database": db_status,
        "port": os.environ.get('PORT', 'Not set'),
        "message": "Cabinet d'Avocats is running"
    })