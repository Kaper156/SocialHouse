from django.db import models

from applications.receptionist.meter.enums import MeterTypesEnum
from applications.receptionist.meter.models import MeterData
from utils.datetime import year_start, year_end


class MeterStatistic(models.Model):
    class Meta:
        verbose_name = "Статистика показаний потребления коммунальных услуг"

    date_of_formation = models.DateField(verbose_name="Дата формирования статистики", )
    date_from = models.DateField(verbose_name="Начало периода", default=year_start)
    date_to = models.DateField(verbose_name="Конец периода", default=year_end)

    meter_type = models.CharField(verbose_name="Тип счётчика", choices=MeterTypesEnum.choices, max_length=1)
    meter_data_for_period = models.ManyToManyField(verbose_name="Показания за период", to=MeterData,
                                                   help_text="Оставьте пустым для автозаполнения на основании периода")
