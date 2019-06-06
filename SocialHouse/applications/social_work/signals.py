from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import ServiceJournal, SERVICE_TYPES
from .utils import get_date_range_around

from applications.core.models import Worker


# Проверка частоты оказания услуги
def check_service_journal_period(instance):
    # Получить родительский SERVICE_TYPE
    instance.type_of_service = instance.service.type_of_service

    # Период дат, для типа периодизации (Неделя\месяц\год ..)
    d_from, d_to = get_date_range_around(instance.date_in, instance.type_of_service)
    _count = ServiceJournal.objects.filter(date_of__range=(d_from, d_to)).count()
    if _count > instance.service.period.count:
        # Услуга становится платной при превышении частоты оказания услуги
        instance.type_of_service = SERVICE_TYPES[2][0]


@receiver(pre_save, sender=ServiceJournal)
def create_service_journal(sender, instance, created, **kwargs):
    check_service_journal_period(instance)
