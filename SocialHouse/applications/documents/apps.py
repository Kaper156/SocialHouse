from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    name = 'applications.documents'
    verbose_name = 'Документация'

    def ready(self):
        pass
