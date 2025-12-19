#!/usr/bin/env python
"""
Script pour créer un superutilisateur sur Railway
Usage: railway run python create_superuser_railway.py
"""
import os
import sys
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Crée un superutilisateur pour Railway"""
    User = get_user_model()
    
    # Informations du superutilisateur
    username = 'admin'
    email = 'admin@cabinet.com'
    password = 'Admin123!'  # Mot de passe temporaire - à changer après connexion
    
    print("🔧 Création du superutilisateur Railway...")
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        print(f"⚠️ L'utilisateur '{username}' existe déjà")
        user = User.objects.get(username=username)
        print(f"✅ Utilisateur existant: {user.username} ({user.email})")
        return user
    
    # Créer le superutilisateur
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superutilisateur créé avec succès!")
        print(f"👤 Username: {username}")
        print(f"📧 Email: {email}")
        print(f"🔒 Password: {password}")
        print(f"⚠️ IMPORTANT: Changez le mot de passe après la première connexion!")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return None

def main():
    """Fonction principale"""
    print("🚀 Création Superutilisateur Railway - Cabinet Avocat")
    print("=" * 60)
    
    try:
        user = create_superuser()
        
        if user:
            print("\n" + "=" * 60)
            print("🎉 SUPERUTILISATEUR PRÊT!")
            print("=" * 60)
            print(f"🌐 Accédez à votre site Railway")
            print(f"🔗 URL Admin: https://votre-site.railway.app/admin")
            print(f"👤 Username: admin")
            print(f"🔒 Password: Admin123!")
            print(f"⚠️ Changez le mot de passe après connexion!")
            
            return True
        else:
            print("\n❌ Échec de la création du superutilisateur")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)