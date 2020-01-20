import datetime

from django.db import models

from applications.core.models import ServicedPerson
from .visit import Visitor


class OvernightJournal(models.Model):
    class Meta:
        verbose_name = "Журнал ночующих в отделении"
        verbose_name_plural = "Журналы ночующих в отделении"

    date_of = models.DateTimeField(verbose_name="Период от", default=datetime.datetime.now)
    date_to = models.DateTimeField(verbose_name="Период до")


class Overnight(models.Model):
    class Meta:
        verbose_name = "Ночующие в отделении"

    journal = models.ForeignKey(verbose_name="Журнал ночующих в отделении", to='OvernightJournal',
                                on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата", default=datetime.datetime.now)


class ServicedPersonOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении обслуживаемый"
        verbose_name_plural = "Ночующие в отделении обслуживаемые"

    overnight = models.ForeignKey(verbose_name="Ночь", to='Overnight', on_delete=models.CASCADE)
    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to=ServicedPerson, on_delete=models.CASCADE)


class VisitorOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении посетитель"
        verbose_name_plural = "Ночующие в отделении посетители"

    overnight = models.ForeignKey(verbose_name="Ночь", to='Overnight', on_delete=models.CASCADE)
    serviced_person = models.ForeignKey(verbose_name="Посетитель", to=Visitor, on_delete=models.CASCADE)
