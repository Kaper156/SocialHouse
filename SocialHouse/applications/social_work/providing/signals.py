from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import ProvidedService


def check_service_journal_period(instance):
    pass
    # # Получить родительский SERVICE_TYPE
    # instance.type_of_service = instance.service.type_of_service
    #
    # # Период дат, для типа периодизации (Неделя\месяц\год ..)
    # d_from, d_to = get_date_range_around(instance.date_in, instance.type_of_service)
    # _count = ProvidedService.objects.filter(date_of__range=(d_from, d_to)).count()
    # if _count > instance.service.period.count:
    #     # Услуга становится платной при превышении частоты оказания услуги
    #     instance.type_of_service = ServiceTypeEnum.PAID


@receiver(pre_save, sender=ProvidedService)
def create_service_journal(sender, instance, created, **kwargs):
    check_service_journal_period(instance)
