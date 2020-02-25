import datetime

from django.db import models

from applications.core.models import WorkerPosition, ExtendedPerson
from applications.core.utils.datetime import later_two_hours


class Visit(models.Model):
    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"

    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE)
    visitor = models.ForeignKey(verbose_name="Посетитель", to='Visitor', on_delete=models.CASCADE)
    date_of = models.DateTimeField(verbose_name="Начало визита", default=datetime.datetime.now)
    date_to = models.DateTimeField(verbose_name="Конец визита", blank=True, null=True, default=later_two_hours)


class Visitor(ExtendedPerson):
    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

    commentary = models.TextField(verbose_name="Комментарий", max_length=2048)
