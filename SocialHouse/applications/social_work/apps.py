from django.apps import AppConfig


class SocialWorkConfig(AppConfig):
    name = 'applications.social_work'
    verbose_name = 'Социальная работа'

    def ready(self):
        import applications.social_work.signals
