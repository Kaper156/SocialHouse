import datetime

from django.core import validators
from django.db import models

from applications.people.models.abstract import Journal
from applications.social_work.ippsu.models import IPPSU
from applications.social_work.limitations.utils.datetime import range_by_period_name
from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service
from .managers import ProvidedServiceByTypeManger


class ProvidedServiceJournal(Journal):
    class Meta:
        verbose_name = "Журнал оказанных услуг"
        verbose_name_plural = "Журналы оказанных услуг"

    ippsu = models.ForeignKey(verbose_name="ИППСУ", to=IPPSU, on_delete=models.CASCADE,
                              related_name="provided_services_journals")

    def __str__(self):
        return f"[{self.period()}] {self.ippsu}"


class ProvidedService(models.Model):
    class Meta:
        verbose_name = "Оказанная услуга"
        verbose_name_plural = "Оказанные услуги"

    journal = models.ForeignKey(verbose_name="Журнал оказанных услуг", to=ProvidedServiceJournal,
                                on_delete=models.CASCADE, related_name="services")
    date_of = models.DateTimeField(verbose_name="Дата оказания", default=datetime.datetime.now)

    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга")

    type_of_service = models.CharField(verbose_name="Тип", choices=ServiceTypeEnum.choices,
                                       max_length=1, default=ServiceTypeEnum.CALCULATING, editable=False)
    volume = models.FloatField(verbose_name="Оказанный объем услуги", default=1.0)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество услуг", default=1,
                                                validators=[validators.MinValueValidator(1)])
    by_type = ProvidedServiceByTypeManger()
    objects = models.Manager()

    def is_from_guaranteed(self):
        return self.service.type_of_service == ServiceTypeEnum.GUARANTEED

    def get_nearby_provided_services(self):
        period_range = range_by_period_name(self.service.period_limitation.period, self.date_of)
        # Todo check is new ippsu.date_from is in period_range
        ippsu = self.journal.ippsu
        nearby_services = ProvidedService.objects.filter(
            journal__ippsu=ippsu,
            date_of__in=period_range
        ).order_by('date_of', 'volume', '-quantity')
        return nearby_services

    def __str__(self):
        return f"[{self.date_of}][{self.service.get_type_of_service_display()[0].upper()}] {self.service}"
