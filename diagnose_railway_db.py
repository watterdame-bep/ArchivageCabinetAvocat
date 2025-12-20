#!/usr/bin/env python3
"""
Script de diagnostic rapide pour Railway MySQL
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.db import connection

def main():
    print("🔍 Diagnostic Railway MySQL")
    print("=" * 40)
    
    # 1. Variables d'environnement
    print("\n📋 Variables MySQL:")
    print(f"  MYSQLHOST: {os.environ.get('MYSQLHOST', 'NON DÉFINIE')}")
    print(f"  MYSQLDATABASE: {os.environ.get('MYSQLDATABASE', 'NON DÉFINIE')}")
    print(f"  MYSQLUSER: {os.environ.get('MYSQLUSER', 'NON DÉFINIE')}")
    print(f"  MYSQLPORT: {os.environ.get('MYSQLPORT', 'NON DÉFINIE')}")
    
    # 2. Test de connexion
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            print(f"\n✅ Connexion MySQL OK - Version: {version}")
    except Exception as e:
        print(f"\n❌ Erreur connexion: {e}")
        return
    
    # 3. Lister les tables
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n📊 Tables dans la base ({len(tables)}):")
            
            if not tables:
                print("  ⚠️ AUCUNE TABLE - Base de données vide!")
                print("  💡 Solution: Exécuter force_migrate_railway.py")
            else:
                auth_tables = []
                django_tables = []
                other_tables = []
                
                # Analyser la casse des tables
                uppercase_tables = []
                lowercase_tables = []
                
                for table in tables:
                    table_name = table[0]
                    
                    # Vérifier la casse
                    if any(c.isupper() for c in table_name):
                        uppercase_tables.append(table_name)
                    else:
                        lowercase_tables.append(table_name)
                    
                    if 'authentification' in table_name.lower():
                        auth_tables.append(table_name)
                    elif 'django' in table_name.lower():
                        django_tables.append(table_name)
                    else:
                        other_tables.append(table_name)
                
                # Diagnostic de casse
                print(f"\n🔍 DIAGNOSTIC CASSE:")
                print(f"  📝 Tables avec majuscules: {len(uppercase_tables)}")
                print(f"  📝 Tables en minuscules: {len(lowercase_tables)}")
                
                if lowercase_tables and not uppercase_tables:
                    print("  ⚠️ PROBLÈME DÉTECTÉ: Toutes les tables sont en minuscules!")
                    print("  💡 Django attend des majuscules (ex: Authentification_compteutilisateur)")
                    print("  💡 Vos tables: minuscules (ex: authentification_compteutilisateur)")
                
                if auth_tables:
                    print(f"\n  ✅ Tables Authentification ({len(auth_tables)}):")
                    for t in auth_tables:
                        expected = "Authentification_compteutilisateur"
                        if t.lower() == expected.lower() and t != expected:
                            print(f"    - {t} ⚠️ (Django attend: {expected})")
                        else:
                            print(f"    - {t}")
                else:
                    print("  ❌ AUCUNE table Authentification trouvée!")
                
                if django_tables:
                    print(f"\n  ✅ Tables Django ({len(django_tables)}):")
                    for t in django_tables[:3]:
                        print(f"    - {t}")
                    if len(django_tables) > 3:
                        print(f"    ... et {len(django_tables)-3} autres")
                
                if other_tables:
                    print(f"\n  📋 Autres tables ({len(other_tables)}):")
                    for t in other_tables[:5]:
                        print(f"    - {t}")
                    if len(other_tables) > 5:
                        print(f"    ... et {len(other_tables)-5} autres")
    
    except Exception as e:
        print(f"\n❌ Erreur listage tables: {e}")
        return
    
    # 4. Test des modèles Django si les tables existent
    if tables:
        try:
            from django.contrib.auth.models import User
            user_count = User.objects.count()
            print(f"\n👥 Utilisateurs Django: {user_count}")
            
            try:
                from Authentification.models import CompteUtilisateur
                compte_count = CompteUtilisateur.objects.count()
                print(f"👤 Comptes utilisateurs: {compte_count}")
            except Exception as e:
                print(f"❌ Erreur modèle CompteUtilisateur: {e}")
                
        except Exception as e:
            print(f"\n❌ Erreur test modèles: {e}")
    
    print(f"\n{'='*40}")
    print("🎯 Résumé:")
    if not tables:
        print("❌ Base vide - Exécuter: python force_migrate_railway.py")
    elif not auth_tables:
        print("❌ Tables manquantes - Exécuter: python force_migrate_railway.py")
    else:
        print("✅ Base de données semble correcte")

if __name__ == '__main__':
    main()