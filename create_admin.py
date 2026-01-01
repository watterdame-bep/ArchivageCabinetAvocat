#!/usr/bin/env python
"""
Créer un superutilisateur pour Railway
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_railway')

django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Créer un superutilisateur"""
    User = get_user_model()
    
    # Vérifier si un superutilisateur existe déjà
    if User.objects.filter(is_superuser=True).exists():
        print("ℹ️ Un superutilisateur existe déjà")
        return
    
    # Créer le superutilisateur
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@cabinet.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superutilisateur créé: {username}")
        print(f"📧 Email: {email}")
        print(f"🔑 Mot de passe: {password}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")

if __name__ == '__main__':
    create_superuser()