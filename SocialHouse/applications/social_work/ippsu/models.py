import datetime

from django.db import models

# Create your models here.
from applications.people.models import WorkerPosition, ServicedPerson
from applications.social_work.services.models import Service
from utils.datetime import later_3_years


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
    included_services = models.ManyToManyField(to=Service, verbose_name="Включенные услуги", blank=True)

    is_archived = models.BooleanField(verbose_name="В архиве",
                                      help_text="Для совместимости со старыми отчетами, "
                                                "установите флаг, вместо удаления ИППСУ",
                                      default=False)

    def __str__(self):
        return f"ИППСУ {self.serviced_person} ({self.social_worker})"

#
# class IncludedService(models.Model):
#     class Meta:
#         verbose_name = "Включенная в ИППСУ услуга"
#         verbose_name_plural = "Включенные в ИППСУ услуги"
#
#     IPPSU = models.ForeignKey(to=IPPSU, on_delete=models.CASCADE, verbose_name="ИППСУ",
#                               related_name="included_services")
#     service = models.ForeignKey(to=Service, on_delete=models.CASCADE, verbose_name="Услуга")
#
#     def __str__(self):
#         return str(self.service)
