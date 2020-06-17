from django.apps import AppConfig


class ContractsConfig(AppConfig):
    name = 'applications.documentation.contracts'
    verbose_name = "Договоры на оказание услуг и ИППСУ"

    def ready(self):
        pass
