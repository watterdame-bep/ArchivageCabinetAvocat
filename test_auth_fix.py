#!/usr/bin/env python3
"""
Test rapide pour vérifier si le problème de casse est résolu
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

def test_authentication():
    """Tester l'accès au modèle CompteUtilisateur"""
    print("🧪 Test d'accès au modèle CompteUtilisateur")
    print("=" * 45)
    
    try:
        from Authentification.models import CompteUtilisateur
        
        # Test 1: Compter les utilisateurs
        print("\n1️⃣ Test comptage utilisateurs:")
        user_count = CompteUtilisateur.objects.count()
        print(f"   ✅ Nombre d'utilisateurs: {user_count}")
        
        # Test 2: Lister quelques utilisateurs
        print("\n2️⃣ Test listage utilisateurs:")
        users = CompteUtilisateur.objects.all()[:5]
        for user in users:
            print(f"   👤 {user.username} - {user.email} - Actif: {user.is_active}")
        
        # Test 3: Vérifier les superusers
        print("\n3️⃣ Test superutilisateurs:")
        admin_count = CompteUtilisateur.objects.filter(is_superuser=True).count()
        print(f"   👑 Nombre d'administrateurs: {admin_count}")
        
        if admin_count > 0:
            admins = CompteUtilisateur.objects.filter(is_superuser=True)[:3]
            for admin in admins:
                print(f"   👑 Admin: {admin.username}")
        
        # Test 4: Vérifier la table utilisée
        print("\n4️⃣ Vérification nom de table:")
        table_name = CompteUtilisateur._meta.db_table
        print(f"   📋 Table Django: {table_name}")
        
        # Test 5: Requête SQL directe
        print("\n5️⃣ Test requête SQL directe:")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            sql_count = cursor.fetchone()[0]
            print(f"   📊 Comptage SQL direct: {sql_count}")
            
            if user_count == sql_count:
                print("   ✅ Cohérence Django ↔ SQL confirmée")
            else:
                print("   ⚠️ Incohérence détectée!")
        
        print(f"\n{'='*45}")
        print("🎉 SUCCÈS: Le modèle CompteUtilisateur fonctionne!")
        print("✅ Le problème de casse des tables est résolu")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("\n💡 Solutions à essayer:")
        print("   1. python fix_table_case_railway.py")
        print("   2. python fix_mysql_case_insensitive.py")
        print("   3. Vérifier l'import des données dans Railway")
        return False

def test_login_simulation():
    """Simuler une tentative de connexion"""
    print("\n🔐 Simulation de connexion")
    print("=" * 30)
    
    try:
        from django.contrib.auth import authenticate
        from Authentification.models import CompteUtilisateur
        
        # Récupérer le premier utilisateur actif
        user = CompteUtilisateur.objects.filter(is_active=True).first()
        
        if user:
            print(f"👤 Test avec utilisateur: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Actif: {user.is_active}")
            print(f"   Staff: {user.is_staff}")
            print(f"   Superuser: {user.is_superuser}")
            
            # Note: On ne peut pas tester le mot de passe sans le connaître
            print("\n💡 Pour tester la connexion complète:")
            print("   - Utilisez l'interface web")
            print("   - Ou créez un nouvel utilisateur de test")
            
        else:
            print("⚠️ Aucun utilisateur actif trouvé")
            
    except Exception as e:
        print(f"❌ Erreur simulation: {e}")

if __name__ == '__main__':
    success = test_authentication()
    
    if success:
        test_login_simulation()
    
    print(f"\n{'='*45}")
    if success:
        print("🚀 Prêt pour le test en production!")
    else:
        print("🔧 Corrections nécessaires avant déploiement")