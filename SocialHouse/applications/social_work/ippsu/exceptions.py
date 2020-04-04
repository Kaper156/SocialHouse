from django.core.exceptions import ValidationError


class ServiceNotIncluded(ValidationError):
    def __init__(self):
        super().__init__("Данная гарантированная услуга не включена в ИППСУ")
