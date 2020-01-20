import datetime

from django.db import models

from applications.core.models import WorkerPosition


class VisitorJournal(models.Model):
    class Meta:
        verbose_name = "Журнал посетителей"
        verbose_name_plural = "Журналы посетителей"

    date_of = models.DateTimeField(verbose_name="Период от", default=datetime.datetime.now)
    date_to = models.DateTimeField(verbose_name="Период до")


class Visit(models.Model):
    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"

    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE)
    visitor = models.ForeignKey(verbose_name="Посетитель", to='Visitor', on_delete=models.CASCADE)
    journal = models.ForeignKey(verbose_name="Журнал посетителей", to='VisitorJournal', on_delete=models.CASCADE)
    date_of = models.DateTimeField(verbose_name="Начало визита", default=datetime.datetime.now)
    # Todo: autoset as 2 hour
    date_to = models.DateTimeField(verbose_name="Конец визита", blank=True, null=True)


class Visitor(models.Model):
    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

    name = models.CharField(verbose_name="Имя", max_length=64)
    patronymic = models.CharField(verbose_name="Имя", max_length=64, blank=True, null=True)
    surname = models.CharField(verbose_name="Имя", max_length=64)
    commentary = models.TextField(verbose_name="Комментарий", max_length=2048)
