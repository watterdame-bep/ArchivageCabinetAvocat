#!/usr/bin/env python3
"""
Solution alternative: Configurer MySQL pour ignorer la casse des tables
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.db import connection

def check_case_sensitivity():
    """Vérifier la configuration de casse MySQL"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
            result = cursor.fetchone()
            if result:
                value = result[1]
                print(f"📋 lower_case_table_names = {value}")
                
                if value == '0':
                    print("  ⚠️ MySQL est sensible à la casse (problématique)")
                    return False
                elif value == '1':
                    print("  ✅ MySQL ignore la casse (optimal)")
                    return True
                elif value == '2':
                    print("  ⚠️ MySQL stocke en minuscule mais compare en casse (mixte)")
                    return False
            else:
                print("❌ Impossible de vérifier la configuration")
                return False
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def test_table_access():
    """Tester l'accès aux tables avec différentes casses"""
    test_cases = [
        ('authentification_compteutilisateur', 'minuscule'),
        ('Authentification_compteutilisateur', 'Django standard'),
        ('AUTHENTIFICATION_COMPTEUTILISATEUR', 'majuscule'),
    ]
    
    print("\n🧪 Test d'accès aux tables:")
    
    for table_name, description in test_cases:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                print(f"  ✅ {description}: {count} enregistrements")
                return table_name  # Retourner le nom qui fonctionne
        except Exception as e:
            print(f"  ❌ {description}: {str(e)[:50]}...")
    
    return None

def create_view_solution():
    """Créer des vues avec la bonne casse comme solution de contournement"""
    print("\n🔧 Création de vues de contournement...")
    
    # Mapping des vues à créer
    views = {
        'Authentification_compteutilisateur': 'authentification_compteutilisateur',
        'Authentification_compteutilisateur_groups': 'authentification_compteutilisateur_groups',
        'Authentification_compteutilisateur_user_permissions': 'authentification_compteutilisateur_user_permissions',
    }
    
    created_count = 0
    
    for view_name, table_name in views.items():
        try:
            with connection.cursor() as cursor:
                # Vérifier si la table source existe
                cursor.execute("SHOW TABLES LIKE %s", [table_name])
                if not cursor.fetchone():
                    print(f"  ⚠️ Table source {table_name} n'existe pas")
                    continue
                
                # Supprimer la vue si elle existe déjà
                cursor.execute(f"DROP VIEW IF EXISTS `{view_name}`")
                
                # Créer la vue
                cursor.execute(f"CREATE VIEW `{view_name}` AS SELECT * FROM `{table_name}`")
                print(f"  ✅ Vue créée: {view_name} → {table_name}")
                created_count += 1
                
        except Exception as e:
            print(f"  ❌ Erreur création vue {view_name}: {e}")
    
    return created_count

def main():
    print("🔧 Solution MySQL Case-Insensitive")
    print("=" * 40)
    
    # 1. Vérifier la configuration MySQL
    print("\n1️⃣ Vérification configuration MySQL:")
    case_insensitive = check_case_sensitivity()
    
    # 2. Tester l'accès aux tables
    working_table = test_table_access()
    
    # 3. Solutions
    print(f"\n{'='*40}")
    print("🎯 Solutions disponibles:")
    
    if working_table:
        print(f"✅ Une table fonctionne: {working_table}")
        
        if not case_insensitive:
            print("\n💡 Solution recommandée: Créer des vues")
            views_created = create_view_solution()
            if views_created > 0:
                print(f"✅ {views_created} vues créées avec succès!")
                print("🔄 Redémarrez l'application pour tester")
            else:
                print("❌ Échec création des vues")
        else:
            print("✅ Configuration MySQL optimale détectée")
    else:
        print("❌ Aucune table accessible - Problème plus grave")
        print("💡 Utilisez fix_table_case_railway.py pour renommer les tables")

if __name__ == '__main__':
    main()