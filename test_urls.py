#!/usr/bin/env python
"""
Script pour tester les URLs de l'application
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.urls import reverse
from django.test import Client

def test_urls():
    """Test des URLs principales"""
    
    print("🔗 Test des URLs de l'application...")
    
    urls_to_test = [
        ('Connexion', 'Page de connexion'),
        ('change_password', 'Changement de mot de passe'),
        ('Deconnecter', 'Déconnexion'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: Erreur - {e}")
    
    print("\n🎯 Test d'accès aux pages (sans authentification)...")
    
    client = Client()
    
    # Test page de connexion (doit être accessible)
    try:
        response = client.get(reverse('Connexion'))
        if response.status_code == 200:
            print("✅ Page de connexion accessible")
        else:
            print(f"⚠️ Page de connexion: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Page de connexion: {e}")
    
    # Test page changement mot de passe (doit rediriger vers login)
    try:
        response = client.get(reverse('change_password'))
        if response.status_code == 302:  # Redirection vers login
            print("✅ Page changement mot de passe protégée (redirection)")
        else:
            print(f"⚠️ Page changement mot de passe: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Page changement mot de passe: {e}")
    
    print("\n🎉 Tests des URLs terminés !")

if __name__ == '__main__':
    test_urls()