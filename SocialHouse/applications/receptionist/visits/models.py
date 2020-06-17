import datetime

from django.db import models

from applications.department.people.models import WorkerPosition, Visitor, WorkerPositionEnum, ServicedPerson
from utils.datetime import later_two_hours


class Visit(models.Model):
    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"

    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'position': WorkerPositionEnum.RECEPTIONIST})
    visitor = models.ForeignKey(verbose_name="Посетитель", to=Visitor, on_delete=models.CASCADE)
    date_of = models.DateTimeField(verbose_name="Начало визита", default=datetime.datetime.now)
    date_to = models.DateTimeField(verbose_name="Конец визита", blank=True, null=True, default=later_two_hours)

    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to=ServicedPerson, on_delete=models.CASCADE)
