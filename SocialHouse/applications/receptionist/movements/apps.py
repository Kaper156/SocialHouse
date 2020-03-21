from django.apps import AppConfig


class MovementsConfig(AppConfig):
    name = 'applications.receptionist.movements'
    verbose_name = "Перемещения обслуживаемых"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)

    def ready(self):
        pass
