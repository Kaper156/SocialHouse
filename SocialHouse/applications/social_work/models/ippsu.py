import datetime

from django.core import validators
from django.db import models

from applications.core.models import ServicedPerson, WorkerPosition
from applications.core.utils.datetime import later_3_years
from .services import Service
from ...core.enums import ServiceTypeEnum
from ...core.models.abstract import Journal


class IPPSU(models.Model):
    class Meta:
        verbose_name = "ИППСУ"
        verbose_name_plural = "ИППСУ"

    social_worker = models.ForeignKey(to=WorkerPosition, on_delete=models.DO_NOTHING,
                                      verbose_name="Социальный работник")
    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.CASCADE,
                                        verbose_name="Обслуживаемый")

    date_from = models.DateField(verbose_name="Действует от", default=datetime.datetime.now)
    date_to = models.DateField(verbose_name="Действителен до", default=later_3_years)

    is_archived = models.BooleanField(verbose_name="В архиве",
                                      help_text="Для совместимости со старыми отчетами, "
                                                "установите флаг, вместо удаления ИППСУ",
                                      default=False)

    def __str__(self):
        return f"ИППСУ {self.serviced_person} ({self.social_worker})"


class IncludedService(models.Model):
    class Meta:
        verbose_name = "Включенная в ИППСУ услуга"
        verbose_name_plural = "Включенные в ИППСУ услуги"

    IPPSU = models.ForeignKey(to='IPPSU', on_delete=models.CASCADE, verbose_name="ИППСУ",
                              related_name="included_services")
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга")

    def __str__(self):
        return str(self.service)


class ProvidedServiceJournal(Journal):
    class Meta:
        verbose_name = "Журнал оказанных услуг"
        verbose_name_plural = "Журналы оказанных услуг"

    ippsu = models.ForeignKey(verbose_name="ИППСУ", to='IPPSU', on_delete=models.CASCADE,
                              related_name="provided_services_journals")

    def save(self, *args, **kwargs):
        # Check by quantity
        for provided in self.services.all():
            state = provided.service.measurement.volume_statement
            if not state:  # Skip services without volume statement
                continue

        super(ProvidedServiceJournal, self).save(*args, **kwargs)

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

    def check_quantity(self):
        statement = self.service.measurement.period_statement
        limit = self.service.measurement.period_statement.limit
        excess = int(statement.get_diff(self.quantity))
        if excess > 0:
            new_type_of_service = self.service.type_of_service

            # Excess guaranteed should be paid
            if self.service.type_of_service == ServiceTypeEnum.GUARANTEED:
                new_type_of_service = ServiceTypeEnum.PAID
            for _ in range(excess):
                # TODO here
                pass

    # TODO rename
    def check_volume(self):
        state = self.service.measurement.volume_statement

        # Excess volume which should be divided
        excess_volume = state.get_diff(self.volume)

        if excess_volume > 0:
            # Max volume per each service
            max_volume = state.limit

            # Count of duplicates (without remainder of division)
            duplicate_count = int(excess_volume // max_volume)

            # Remainder of division
            last_volume = excess_volume - max_volume * duplicate_count

            # Duplicate max_volume
            duplicates_volumes = [max_volume] * duplicate_count

            # Add remainder
            duplicates_volumes.append(last_volume)

            for volume in duplicates_volumes:
                ProvidedService(
                    journal=self.journal,
                    date_of=self.date_of,
                    service=self.service,
                    type_of_service=self.type_of_service,
                    volume=volume,
                    quantity=self.quantity
                )
                pass

    def check_limits(self):
        self.check_quantity()
        self.check_volume()

    # def save(self, *args, **kwargs):
    #     def_type = self.service.type_of_service
    #
    #     # Checking only guaranteed, skip other types
    #     if def_type != ServiceTypeEnum.GUARANTEED:
    #         self.type_of_service = def_type
    #         super(ProvidedService, self).save(*args, **kwargs)
    #
    #     coincidences = self.by_type.custom(type_of_service=def_type) \
    #         .values('service').annotate(count=models.Count('service'))
    #
    #     if coincidences.get(self.service) is None:
    #         self.type_of_service = def_type
    #         super(ProvidedService, self).save(*args, **kwargs)
    #
    #     super(ProvidedService, self).save(*args, **kwargs)

    def __str__(self):
        return f"[{self.date_of}][{self.service.get_type_of_service_display()[0].upper()}] {self.service}"
