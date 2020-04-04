from django.apps import AppConfig


class ProvidingServicesConfig(AppConfig):
    name = 'applications.social_work.providing'
    verbose_name = "Оказание услуг"

    def ready(self):
        pass
