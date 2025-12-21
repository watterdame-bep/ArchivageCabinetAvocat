#!/usr/bin/env python
"""
Test simple et direct des fichiers statiques
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings
from django.template.loader import render_to_string
from django.template import Context, Template
from django.contrib.staticfiles.finders import find

def test_template_rendering():
    """Test du rendu des templates avec les fichiers statiques"""
    
    print("🧪 TEST SIMPLE DES FICHIERS STATIQUES")
    print("=" * 45)
    
    # 1. Test de base
    print("\n📋 CONFIGURATION:")
    print(f"DEBUG = {settings.DEBUG}")
    print(f"STATIC_URL = {settings.STATIC_URL}")
    print(f"STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
    
    # 2. Test de rendu d'un template simple
    print("\n🎨 TEST DE RENDU TEMPLATE:")
    
    template_content = """
    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{% static 'css/style.css' %}">
        <link rel="stylesheet" href="{% static 'css/vendors_css.css' %}">
    </head>
    <body>
        <h1>Test</h1>
        <script src="{% static 'js/vendors.min.js' %}"></script>
    </body>
    </html>
    """
    
    try:
        template = Template(template_content)
        rendered = template.render(Context({}))
        
        print("✅ Template rendu avec succès")
        
        # Extraire les URLs générées
        import re
        css_urls = re.findall(r'href="([^"]*\.css)"', rendered)
        js_urls = re.findall(r'src="([^"]*\.js)"', rendered)
        
        print("\n🔗 URLs GÉNÉRÉES:")
        for url in css_urls:
            print(f"CSS: {url}")
        for url in js_urls:
            print(f"JS:  {url}")
            
        # Vérifier si les URLs sont correctes
        expected_prefix = settings.STATIC_URL
        all_correct = True
        
        for url in css_urls + js_urls:
            if not url.startswith(expected_prefix):
                print(f"❌ URL incorrecte: {url} (devrait commencer par {expected_prefix})")
                all_correct = False
        
        if all_correct:
            print("✅ Toutes les URLs sont correctes")
        
    except Exception as e:
        print(f"❌ Erreur lors du rendu: {e}")
    
    # 3. Test de recherche des fichiers
    print("\n🔍 RECHERCHE DES FICHIERS:")
    files_to_check = [
        'css/style.css',
        'css/vendors_css.css',
        'css/skin_color.css',
        'js/vendors.min.js'
    ]
    
    for file_path in files_to_check:
        found = find(file_path)
        if found:
            print(f"✅ {file_path} trouvé")
        else:
            print(f"❌ {file_path} NON trouvé")
    
    # 4. Instructions pour le test manuel
    print("\n🎯 TEST MANUEL RECOMMANDÉ:")
    print("1. Ouvrez un terminal")
    print("2. Exécutez: python manage.py runserver")
    print("3. Dans votre navigateur, allez sur:")
    print("   http://127.0.0.1:8000/static/css/style.css")
    print("4. Vous devriez voir le contenu CSS, pas une erreur 404")
    print("\n5. Si vous voyez le CSS, le problème est dans les templates")
    print("6. Si vous voyez 404, le problème est dans la configuration Django")
    
    # 5. Test de la configuration URLs
    print("\n🌐 VÉRIFICATION DE LA CONFIGURATION URLS:")
    try:
        with open('CabinetAvocat/urls.py', 'r', encoding='utf-8') as f:
            urls_content = f.read()
            
        if 'STATICFILES_DIRS[0]' in urls_content:
            print("✅ urls.py utilise STATICFILES_DIRS[0] (correct pour DEBUG=True)")
        elif 'STATIC_ROOT' in urls_content:
            print("⚠️ urls.py utilise STATIC_ROOT (peut causer des problèmes en DEBUG=True)")
        else:
            print("❌ Configuration static non trouvée dans urls.py")
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de urls.py: {e}")
    
    print("\n🎉 Test terminé !")
    return True

if __name__ == '__main__':
    test_template_rendering()