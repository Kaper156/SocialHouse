from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'applications.core'
    verbose_name = 'Ядро'

    def ready(self):
        import applications.core.signals
