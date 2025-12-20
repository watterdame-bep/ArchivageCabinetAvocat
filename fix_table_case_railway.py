#!/usr/bin/env python3
"""
Script pour corriger le problème de casse des tables Railway MySQL
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CabinetAvocat.settings_production')
django.setup()

from django.db import connection

# Mapping des tables avec la bonne casse Django
TABLE_MAPPING = {
    # Tables Authentification
    'authentification_compteutilisateur': 'Authentification_compteutilisateur',
    'authentification_compteutilisateur_groups': 'Authentification_compteutilisateur_groups',
    'authentification_compteutilisateur_user_permissions': 'Authentification_compteutilisateur_user_permissions',
    
    # Tables principales (si elles existent)
    'adresse_adresse': 'Adresse_adresse',
    'agent_agent': 'Agent_agent',
    'dossier_dossier': 'Dossier_dossier',
    'structure_structure': 'Structure_structure',
    'paiement_paiement': 'Paiement_paiement',
    'parametre_parametre': 'Parametre_parametre',
    
    # Tables Django (normalement déjà correctes)
    'auth_group': 'auth_group',
    'auth_group_permissions': 'auth_group_permissions',
    'auth_permission': 'auth_permission',
    'auth_user': 'auth_user',
    'auth_user_groups': 'auth_user_groups',
    'auth_user_user_permissions': 'auth_user_user_permissions',
    'django_admin_log': 'django_admin_log',
    'django_content_type': 'django_content_type',
    'django_migrations': 'django_migrations',
    'django_session': 'django_session',
}

def get_existing_tables():
    """Récupérer la liste des tables existantes"""
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        return [table[0] for table in cursor.fetchall()]

def rename_table(old_name, new_name):
    """Renommer une table"""
    try:
        with connection.cursor() as cursor:
            # Vérifier que l'ancienne table existe
            cursor.execute("SHOW TABLES LIKE %s", [old_name])
            if not cursor.fetchone():
                print(f"  ⚠️ Table {old_name} n'existe pas")
                return False
            
            # Vérifier que la nouvelle table n'existe pas déjà
            cursor.execute("SHOW TABLES LIKE %s", [new_name])
            if cursor.fetchone():
                print(f"  ⚠️ Table {new_name} existe déjà")
                return False
            
            # Renommer
            cursor.execute(f"RENAME TABLE `{old_name}` TO `{new_name}`")
            print(f"  ✅ {old_name} → {new_name}")
            return True
            
    except Exception as e:
        print(f"  ❌ Erreur renommage {old_name}: {e}")
        return False

def main():
    print("🔧 Correction de la casse des tables Railway MySQL")
    print("=" * 55)
    
    # 1. Lister les tables existantes
    existing_tables = get_existing_tables()
    print(f"\n📋 Tables existantes ({len(existing_tables)}):")
    
    lowercase_tables = []
    for table in existing_tables:
        if any(c.isupper() for c in table):
            print(f"  ✅ {table} (casse correcte)")
        else:
            print(f"  ⚠️ {table} (minuscule)")
            lowercase_tables.append(table)
    
    if not lowercase_tables:
        print("\n✅ Aucun problème de casse détecté!")
        return
    
    print(f"\n🔧 Tables à corriger ({len(lowercase_tables)}):")
    
    # 2. Renommer les tables problématiques
    renamed_count = 0
    for old_name in lowercase_tables:
        if old_name in TABLE_MAPPING:
            new_name = TABLE_MAPPING[old_name]
            print(f"\n🔄 Renommage: {old_name} → {new_name}")
            if rename_table(old_name, new_name):
                renamed_count += 1
        else:
            print(f"\n⚠️ Mapping non défini pour: {old_name}")
    
    print(f"\n{'='*55}")
    print(f"🎯 Résumé: {renamed_count} tables renommées avec succès")
    
    if renamed_count > 0:
        print("✅ Problème de casse corrigé!")
        print("🔄 Redémarrez l'application pour tester")
    else:
        print("❌ Aucune table n'a pu être renommée")

if __name__ == '__main__':
    main()