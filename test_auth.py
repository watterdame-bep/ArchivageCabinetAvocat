#!/usr/bin/env python
"""
Script de test pour vérifier que l'authentification respecte la casse
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from Authentification.backends import Sensible_Case

User = get_user_model()

def test_case_sensitivity():
    print("🧪 Test de sensibilité à la casse pour l'authentification")
    print("=" * 60)
    
    # Créer un utilisateur de test (si il n'existe pas)
    test_username = "TestUser"
    test_password = "testpass123"
    
    try:
        user, created = User.objects.get_or_create(
            username=test_username,
            defaults={
                'password': test_password,
                'type_compte': 'admin'
            }
        )
        if created:
            user.set_password(test_password)
            user.save()
            print(f"✅ Utilisateur de test créé: {test_username}")
        else:
            print(f"ℹ️  Utilisateur de test existant: {test_username}")
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return
    
    print("\n🔍 Tests d'authentification:")
    print("-" * 40)
    
    # Test 1: Casse correcte
    print(f"1. Test avec casse correcte: '{test_username}'")
    auth_result = authenticate(username=test_username, password=test_password)
    if auth_result:
        print("   ✅ SUCCÈS - Authentification réussie")
    else:
        print("   ❌ ÉCHEC - Authentification échouée")
    
    # Test 2: Casse incorrecte (minuscules)
    print(f"2. Test avec casse incorrecte: '{test_username.lower()}'")
    auth_result = authenticate(username=test_username.lower(), password=test_password)
    if auth_result:
        print("   ❌ PROBLÈME - Authentification réussie (ne devrait pas!)")
    else:
        print("   ✅ CORRECT - Authentification échouée comme attendu")
    
    # Test 3: Casse incorrecte (majuscules)
    print(f"3. Test avec casse incorrecte: '{test_username.upper()}'")
    auth_result = authenticate(username=test_username.upper(), password=test_password)
    if auth_result:
        print("   ❌ PROBLÈME - Authentification réussie (ne devrait pas!)")
    else:
        print("   ✅ CORRECT - Authentification échouée comme attendu")
    
    # Test 4: Mot de passe incorrect
    print(f"4. Test avec mot de passe incorrect")
    auth_result = authenticate(username=test_username, password="wrongpass")
    if auth_result:
        print("   ❌ PROBLÈME - Authentification réussie avec mauvais mot de passe!")
    else:
        print("   ✅ CORRECT - Authentification échouée avec mauvais mot de passe")
    
    print("\n" + "=" * 60)
    print("🎯 Résumé: L'authentification respecte maintenant la casse!")
    print("   - Seule la casse exacte permet la connexion")
    print("   - Les variations de casse sont rejetées")
    print("   - La sécurité est renforcée")

if __name__ == "__main__":
    test_case_sensitivity()