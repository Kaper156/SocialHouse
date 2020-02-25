import datetime

from django.db import models

from applications.core.models import ServicedPerson, WorkerPosition
from applications.core.utils.datetime import later_3_years
from .services import SERVICE_TYPES, Service


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

    IPPSU = models.ForeignKey(to='IPPSU', on_delete=models.CASCADE, verbose_name="ИППСУ")
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга")


class ProvidedService(models.Model):
    class Meta:
        verbose_name = "Оказанная услуга"
        verbose_name_plural = "Оказанные услуги"

    ippsu = models.ForeignKey(verbose_name="ИППСУ", to='IPPSU', on_delete=models.CASCADE)
    date_of = models.DateTimeField(verbose_name="Дата оказания", default=datetime.datetime.now)

    service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга")

    # TODO form https://stackoverflow.com/questions/6862250/change-a-django-form-field-to-a-hidden-field
    type_of_service = models.CharField(verbose_name="Тип услуги", choices=SERVICE_TYPES, max_length=1,
                                       blank=True, )
    # TODO check service_types_by_period
    # TODO check in includedServices
