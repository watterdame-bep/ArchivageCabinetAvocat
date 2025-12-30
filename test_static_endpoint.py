
# Ajouter à urls.py pour tester les fichiers statiques
from django.http import JsonResponse
from django.conf import settings
import os

def test_static_files(request):
    """Endpoint pour tester la disponibilité des fichiers statiques"""
    static_root = settings.STATIC_ROOT
    
    test_files = [
        'css/style.css',
        'css/vendors_css.css',
        'assets/vendor_components/bootstrap/dist/css/bootstrap.css'
    ]
    
    results = {}
    for file_path in test_files:
        full_path = os.path.join(static_root, file_path)
        results[file_path] = {
            'exists': os.path.exists(full_path),
            'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0,
            'full_path': full_path
        }
    
    return JsonResponse({
        'static_root': static_root,
        'static_url': settings.STATIC_URL,
        'files': results
    })

# Ajouter cette ligne à urlpatterns:
# path('test-static/', test_static_files, name='test_static'),
