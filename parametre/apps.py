from django.apps import AppConfig


class ParametreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parametre'

    def ready(self):
        import parametre.signal #import le fichier signals