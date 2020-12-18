from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    name = 'apps.profiles'

    def ready(self):
        import django_refresher.src.apps.profiles.signals

