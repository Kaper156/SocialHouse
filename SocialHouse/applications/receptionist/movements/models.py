import datetime

from django.db import models

from applications.department.people.models import ServicedPerson, Visitor


class Leaving(models.Model):
    class Meta:
        abstract = True

    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.CASCADE, verbose_name="Обслуживаемый")
    date_from = models.DateField(verbose_name="От", default=datetime.datetime.now)
    date_to = models.DateField(verbose_name="До", blank=True, null=True)
    commentary = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        result = f"{self.serviced_person} от {self.date_from}"
        if self.date_to:
            result += f" до {self.date_to}"
        return result


class Travel(Leaving):
    class Meta:
        verbose_name = "Поездка обслуживаемого"
        verbose_name_plural = "Поездки обслуживаемых"

    visitor = models.ForeignKey(verbose_name="Родственник", to=Visitor, blank=True, null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        result = "Поездка " + super().__str__()
        if self.visitor:
            result += f" к {self.visitor}"
        return result


class SickLeave(Leaving):
    class Meta:
        verbose_name = "Больничный"
        verbose_name_plural = "Больничные"

    diagnose = models.TextField(verbose_name="Диагноз", blank=True, null=True)

    def __str__(self):
        result = "Больничный " + super().__str__()
        if self.diagnose and len(self.diagnose) < 15:
            result += f" ({self.diagnose})"
        return result
