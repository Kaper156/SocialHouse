import datetime

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.utils import dateformat

from applications.documentation.contracts.models import IPPSU, SocialContract, PaidContract
from applications.social_work.limitations.utils.datetime import range_by_period_name
from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service
from utils.datetime import month_start, month_end
from .managers import ProvidedServiceByTypeManger
from ...documentation.contracts.enums import ContractStatusEnum


class ProvidedJournal(models.Model):
    class Meta:
        verbose_name = "Журнал оказанных услуг"
        verbose_name_plural = "Журналы оказанных услуг"

    ippsu = models.ForeignKey(verbose_name="ИППСУ", to=IPPSU, on_delete=models.CASCADE,
                              related_name="provided_journals")

    contract_social = models.ForeignKey(verbose_name="Договор на оказание социальных услуг", to=SocialContract,
                                        related_name="provided_journals", on_delete=models.CASCADE)
    contract_paid = models.ForeignKey(verbose_name="Договор на оказание платных услуг", to=PaidContract,
                                      related_name="provided_journals", on_delete=models.CASCADE)

    date_from = models.DateField(verbose_name="Период от", default=month_start)
    date_to = models.DateField(verbose_name="Период до", default=month_end)

    def period(self):
        return dateformat.format(self.date_from, 'Y-m F')

    period.short_description = "Период"

    def services_count(self):
        return self.services.count()

    def clean(self):
        contracts = self.ippsu, self.contract_social, self.contract_paid
        # TODO with filter func
        if not all(el.serviced_person == contracts[0].serviced_person for el in contracts):
            raise ValidationError("Один из договоров либо ИППСУ заключены с другим обслуживаемым")
        if not all(el.executor == contracts[0].executor for el in contracts):
            raise ValidationError("Один из договоров либо ИППСУ заключены с другим исполнителем")

        # IPPSU date check
        if self.ippsu.date_expiration < self.date_to:
            raise ValidationError(f"Действие ИППСУ заканчивается ранее действия журнала: {self.ippsu.date_expiration}")
        if self.ippsu.date_from > self.date_from:
            raise ValidationError(f"Действие ИППСУ начинается позднее действия журнала: {self.ippsu.date_expiration}")

        # Contract social date check
        if self.contract_social.date_from > self.date_from:
            raise ValidationError(f"Действие договора социальных услуг начинается позднее "
                                  f"действия журнала: {self.contract_social.date_to}")
        if self.contract_social.date_expiration and self.contract_social.date_expiration < self.date_to:
            raise ValidationError(f"Действие договора платных услуг заканчивается раньше чем действие журнала: "
                                  f"{self.contract_social.date_expiration}")
        # Contract paid date check
        if self.contract_paid.date_from > self.date_from:
            raise ValidationError(f"Действие договора платных услуг начинается позднее "
                                  f"действия журнала: {self.contract_paid.date_to}")
        if self.contract_paid.date_expiration and self.contract_paid.date_expiration < self.date_to:
            raise ValidationError(f"Действие договора платных услуг заканчивается раньше чем действие журнала: "
                                  f"{self.contract_paid.date_expiration}")

    # TODO delete or huge refactoring
    # Maybe move to business layer
    def get_aggregated_rows(self, type_of_service: ServiceTypeEnum) -> list:
        '''
        Get rows for standardization
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

    journal = models.ForeignKey(verbose_name="Журнал оказанных услуг", to=ProvidedJournal,
                                on_delete=models.CASCADE, related_name="services")
    date_of = models.DateTimeField(verbose_name="Дата оказания", default=datetime.datetime.now)

    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга",
                                limit_choices_to={'is_archived': False})

    type_of_service = models.CharField(verbose_name="Тип", choices=ServiceTypeEnum.choices,
                                       max_length=1, default=ServiceTypeEnum.CALCULATING, editable=False)
    volume = models.FloatField(verbose_name="Оказанный объем услуги", default=1.0)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество услуг", default=1,
                                                validators=[validators.MinValueValidator(1)])
    by_type = ProvidedServiceByTypeManger()
    objects = models.Manager()

    def clean(self):
        # Check dates
        if self.date_of < self.journal.date_from or self.date_of > self.journal.date_to:
            raise ValidationError(f"Дата должна быть в диапозоне действия журнала "
                                  f"(от {self.journal.date_from} до {self.journal.date_to})")

        type_of_service = self.service.type_of_service
        # If social service
        if type_of_service == ServiceTypeEnum.GUARANTEED or type_of_service == ServiceTypeEnum.ADDITIONAL:
            if self.journal.contract_social.contract_status != ContractStatusEnum.ACTIVE:
                raise ValidationError(f"Договор на оказание социальных услуг приостановлен либо прекращен")
        # If guaranteed service
        if type_of_service == ServiceTypeEnum.GUARANTEED:
            if self.journal.ippsu.contract_status != ContractStatusEnum.ACTIVE:
                raise ValidationError(f"ИППСУ обслуживаемого приостановлен либо прекращен")
            # Check this
            # Check service in ippsu
            if self.service not in self.journal.ippsu.included_services:
                raise ValidationError(f"Данная услуга не включена в ИППСУ")
        # If paid service
        if type_of_service == ServiceTypeEnum.PAID:
            if self.journal.ippsu.contract_status != ContractStatusEnum.ACTIVE:
                raise ValidationError(f"Договор на оказание платных услуг приостановлен либо прекращен")

    # TODO delete and move to BL
    def is_from_guaranteed(self):
        return self.service.type_of_service == ServiceTypeEnum.GUARANTEED

    # TODO delete or huge refactoring
    # Maybe move to business layer
    def get_nearby_provided_services(self):
        period_range = range_by_period_name(self.service.period_limitation.period, self.date_of)
        # Todo check is new contracts.date_from is in period_range
        ippsu = self.journal.ippsu
        nearby_services = ProvidedService.objects.filter(
            journal__ippsu=ippsu,
            date_of__in=period_range
        ).order_by('date_of', 'volume', '-quantity')
        return nearby_services

    def __str__(self):
        return f"[{self.date_of}][{self.service.get_type_of_service_display()[0].upper()}] {self.service}"
