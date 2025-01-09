from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # automatically create and save a Profile instance whenever a User is created
    def ready(self):
        import users.signals  # Import the signals module
