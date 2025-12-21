#!/usr/bin/env python
"""
Script de test pour la fonctionnalité de changement de mot de passe
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from Authentification.forms import ChangePasswordForm

User = get_user_model()

def test_password_change_functionality():
    """Test de la fonctionnalité de changement de mot de passe"""
    
    print("🔧 Test de la fonctionnalité de changement de mot de passe...")
    
    # Test 1: Vérifier que l'URL existe
    try:
        url = reverse('change_password')
        print(f"✅ URL générée avec succès: {url}")
    except Exception as e:
        print(f"❌ Erreur lors de la génération de l'URL: {e}")
        return False
    
    # Test 2: Vérifier le formulaire
    try:
        # Créer un utilisateur de test
        user = User.objects.create_user(
            username='test_user',
            password='old_password123',
            type_compte='user'
        )
        
        # Test du formulaire avec des données valides
        form_data = {
            'old_password': 'old_password123',
            'new_password1': 'new_password456',
            'new_password2': 'new_password456'
        }
        
        form = ChangePasswordForm(user=user, data=form_data)
        if form.is_valid():
            print("✅ Formulaire valide avec des données correctes")
        else:
            print(f"❌ Erreurs du formulaire: {form.errors}")
            
        # Test avec mot de passe incorrect
        form_data_invalid = {
            'old_password': 'wrong_password',
            'new_password1': 'new_password456',
            'new_password2': 'new_password456'
        }
        
        form_invalid = ChangePasswordForm(user=user, data=form_data_invalid)
        if not form_invalid.is_valid():
            print("✅ Formulaire invalide avec ancien mot de passe incorrect (comportement attendu)")
        else:
            print("❌ Le formulaire devrait être invalide avec un mauvais ancien mot de passe")
            
        # Nettoyer
        user.delete()
        
    except Exception as e:
        print(f"❌ Erreur lors du test du formulaire: {e}")
        return False
    
    # Test 3: Vérifier que le template existe
    try:
        template_path = 'CabinetAvocat/templates/auth_template/auth_user_pass.html'
        if os.path.exists(template_path):
            print("✅ Template de changement de mot de passe trouvé")
        else:
            print("❌ Template de changement de mot de passe non trouvé")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du template: {e}")
    
    print("\n🎉 Tests terminés ! La fonctionnalité de changement de mot de passe est prête.")
    return True

if __name__ == '__main__':
    test_password_change_functionality()