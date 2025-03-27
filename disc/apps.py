from django.apps import AppConfig

class DiscConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'disc'

    # Load signals for matching
    def ready(self):
        import disc.signals