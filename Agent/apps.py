from django.apps import AppConfig


class AgentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Agent'
    
    def ready(self):
        # Importer les signaux pour qu'ils soient enregistrés
        import Agent.signals