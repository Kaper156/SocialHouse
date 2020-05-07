from django.apps import AppConfig


class ActsConfig(AppConfig):
    name = 'applications.social_work.acts'
    verbose_name = "Акты оказанных услуг"

    def ready(self):
        pass
