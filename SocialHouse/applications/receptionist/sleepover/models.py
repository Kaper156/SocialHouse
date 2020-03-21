import datetime

from django.db import models

from applications.people.models import ServicedPerson, WorkerPosition, Visitor


class NightShift(models.Model):
    class Meta:
        verbose_name = "Ночная смена"
        verbose_name_plural = "Ночные смены"

    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата", default=datetime.datetime.now)


class ServicedPersonOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении обслуживаемый"
        verbose_name_plural = "Ночующие в отделении обслуживаемые"

    overnight = models.ForeignKey(verbose_name="Ночь", to=NightShift, on_delete=models.CASCADE)
    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to=ServicedPerson, on_delete=models.CASCADE)


class VisitorOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении посетитель"
        verbose_name_plural = "Ночующие в отделении посетители"

    overnight = models.ForeignKey(verbose_name="Ночь", to=NightShift, on_delete=models.CASCADE)
    serviced_person = models.ForeignKey(verbose_name="Посетитель", to=Visitor, on_delete=models.CASCADE)
