from django.db import models

from applications.social_work.services.enums import ServiceTypeEnum


class ProvidedServiceByTypeManger(models.Manager):
    def custom(self, type_of_service: ServiceTypeEnum):
        return super().get_queryset().filter(type_of_service=type_of_service)

    def guaranteed(self):
        # Not include 'calculating', because they will be set after
        return super().get_queryset().filter(type_of_service__in=ServiceTypeEnum.GUARANTEED)

    def additional(self):
        return super().get_queryset().filter(type_of_service=ServiceTypeEnum.ADDITIONAL)

    def paid(self):
        # Include 'paid from guaranteed' therefore, because they maked from over period limit
        return super().get_queryset().filter(type_of_service__in=[ServiceTypeEnum.PAID,
                                                                  ServiceTypeEnum.PAID_FROM_GUARANTEED])
