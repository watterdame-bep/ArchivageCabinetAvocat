# Generated manually for safe deployment
from django.db import migrations, connection


def safe_cleanup_activity_models(apps, schema_editor):
    """
    Supprime les anciens modèles d'activité seulement s'ils existent
    """
    with connection.cursor() as cursor:
        # Vérifier si les tables existent avant de les supprimer
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'Agent_activitylog'
        """)
        
        if cursor.fetchone()[0] > 0:
            # La table existe, on peut la supprimer
            cursor.execute("DROP TABLE IF EXISTS Agent_activitylog")
        
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'Agent_simpleactivitylog'
        """)
        
        if cursor.fetchone()[0] > 0:
            # La table existe, on peut la supprimer
            cursor.execute("DROP TABLE IF EXISTS Agent_simpleactivitylog")


def reverse_cleanup(apps, schema_editor):
    """
    Fonction de retour - ne fait rien car on ne peut pas recréer les anciennes tables
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0005_simple_activity_log'),
    ]

    operations = [
        migrations.RunPython(safe_cleanup_activity_models, reverse_cleanup),
    ]