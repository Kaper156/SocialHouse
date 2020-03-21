from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'applications.website.news'
    verbose_name = 'Новости'

    def ready(self):
        pass
