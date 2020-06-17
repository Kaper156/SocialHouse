from django.apps import AppConfig


class StandardizationConfig(AppConfig):
    name = 'applications.documentation.standardization'
    verbose_name = 'Шаблонизация'

    def ready(self):
        pass
