from django.apps import AppConfig


class LeavingConfig(AppConfig):
    name = 'applications.leaving'
    verbose_name = "Поездки и больничные обслуживаемых"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)

    def ready(self):
        import applications.leaving.signals
