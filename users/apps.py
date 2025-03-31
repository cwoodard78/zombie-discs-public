from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Automatically create and save a Profile instance whenever a User is created by importing the signal handlers  
        """
        import users.signals