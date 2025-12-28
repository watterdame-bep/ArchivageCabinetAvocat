# Generated manually for ActivityLog model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Agent', '0003_add_activity_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('action', models.CharField(choices=[('create', 'Création'), ('update', 'Modification'), ('delete', 'Suppression'), ('view', 'Consultation'), ('payment', 'Paiement'), ('assign', 'Attribution'), ('close', 'Clôture'), ('reopen', 'Réouverture')], max_length=20)),
                ('entity_type', models.CharField(choices=[('dossier', 'Dossier'), ('declaration', 'Déclaration'), ('document', 'Document'), ('paiement', 'Paiement'), ('client', 'Client'), ('agent', 'Agent'), ('piece_justificative', 'Pièce justificative')], max_length=30)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('extra_data', models.JSONField(blank=True, default=dict)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['user', '-timestamp'], name='Agent_activ_user_id_b8e5a5_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['entity_type', '-timestamp'], name='Agent_activ_entity__c8a9b1_idx'),
        ),
        migrations.AddIndex(
            model_name='activitylog',
            index=models.Index(fields=['action', '-timestamp'], name='Agent_activ_action_4f8c2d_idx'),
        ),
    ]