import datetime

from django.db import models

from applications.core.models import WorkerPosition

METER_TYPES = (
    ('C', "Холодная вода"),
    ('W', "Горячая вода"),
    ('G', "Газосноснабжение"),
    ('E', "Электричество"),
    ('O', "Отопление"),
)


class Meter(models.Model):
    class Meta:
        verbose_name = "Счётчик"
        verbose_name_plural = "Счётчики"

    meter_type = models.CharField(verbose_name="Тип счётчика", choices=METER_TYPES, max_length=1)
    serial_number = models.CharField(verbose_name="Серийный номер счетчика", max_length=64, )


class SealingMeter(models.Model):
    class Meta:
        verbose_name_plural = "Опломбировка счётчика"
        verbose_name = "Опломбировки счётчиков"

    meter = models.ForeignKey(verbose_name="Счётчик", to='Meter', on_delete=models.CASCADE)
    date_of = models.DateField(verbose_name="Опломбирован", default=datetime.datetime.now)
    date_to = models.DateField(verbose_name="Опломбирование действительно до")


class MeterData(models.Model):
    class Meta:
        verbose_name = "Показания счётчика"
        verbose_name_plural = "Показания счётчиков"

    sealing_meter = models.ForeignKey(verbose_name="Опломбировка", to='SealingMeter', on_delete=models.CASCADE)
    # journal = models.ForeignKey(verbose_name="Журнал потребления коммунальных услуг", to='MeterDataJournal',
    #                             on_delete=models.CASCADE)
    data = models.DecimalField(verbose_name="Показания", max_digits=15, decimal_places=1)
    date_of = models.DateField(verbose_name="Дата показания", default=datetime.datetime.now)
    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE)


class UtilityBil(models.Model):
    class Meta:
        verbose_name = "Квитанция коммунальных услуг"
        verbose_name_plural = "Квитанции коммунальных услуг"

    date_of = models.DateField(verbose_name="Дата начисления", default=datetime.datetime.now)
    total = models.DecimalField(verbose_name="Сумма", max_digits=15, decimal_places=5)
    chief = models.ForeignKey(verbose_name="Ответственный заведующий", to=WorkerPosition,
                              on_delete=models.CASCADE)
    sealing_meter = models.ForeignKey(verbose_name="Опломбировка", to='SealingMeter', on_delete=models.DO_NOTHING)
