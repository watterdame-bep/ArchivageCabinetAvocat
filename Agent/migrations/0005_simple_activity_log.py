# Generated manually for simple ActivityLog

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0004_activitylog'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),  # Stocker le nom d'utilisateur directement
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('action', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=50, default='mdi-information')),
                ('color', models.CharField(max_length=20, default='secondary')),
                ('dossier_id', models.IntegerField(null=True, blank=True)),
                ('extra_data', models.JSONField(default=dict, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
