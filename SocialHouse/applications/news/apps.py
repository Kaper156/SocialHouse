from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'applications.news'
    verbose_name = 'Новости'

    def ready(self):
        import applications.news.signals
