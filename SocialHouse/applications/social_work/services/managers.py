from django.db import models

from .enums import ServiceTypeEnum


class ServiceByTypeManger(models.Manager):
    def custom(self, type_of_service: ServiceTypeEnum):
        return super().get_queryset().filter(type_of_service=type_of_service)

    def guaranteed(self):
        return super().get_queryset().filter(type_of_service=ServiceTypeEnum.GUARANTEED)

    def additional(self):
        return super().get_queryset().filter(type_of_service=ServiceTypeEnum.ADDITIONAL)

    def paid(self):
        return super().get_queryset().filter(type_of_service=ServiceTypeEnum.PAID)
