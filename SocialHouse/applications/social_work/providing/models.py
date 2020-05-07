import datetime

from django.core import validators
from django.db import models
from django.db.models import Sum, F

from applications.social_work.ippsu.models import IPPSU
from applications.social_work.limitations.utils.datetime import range_by_period_name
from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service
from .managers import ProvidedServiceByTypeManger
from ...documents.models.base import Journal


class ProvidedServiceJournal(Journal):
    class Meta:
        verbose_name = "Журнал оказанных услуг"
        verbose_name_plural = "Журналы оказанных услуг"

    ippsu = models.ForeignKey(verbose_name="ИППСУ", to=IPPSU, on_delete=models.CASCADE,
                              related_name="provided_services_journals")

    def get_aggregated_rows(self, type_of_service: ServiceTypeEnum) -> list:
        '''
        Get rows for documents
        :param type_of_service: type of service which is usually GUARANTEED, ADDITIONAL, PAID
        :return: list of dicts contain these fields: service_id, title, tax, quantity, volume, total (tax*quantity)
        '''
        result_set = list(self.services.filter(type_of_service=type_of_service)
                          .annotate(title=F('service__title'), tax=F('service__tax'))  # Rename as short as possible
                          .values('service_id', 'title', 'tax', )  # Group by service
                          .annotate(quantity=Sum('quantity'), volume=Sum('volume')))  # Aggregate
        for service in result_set:
            service['total'] = service['tax'] * service['quantity']
        return result_set

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
