import datetime

from django.db import models

from applications.social_work.limitations.models import VolumeLimitation, PeriodLimitation, get_one_volume
from applications.social_work.services.managers import ServiceByTypeManger
from .enums import ServiceTypeEnum, ServiceCategoryEnum


class ServiceMeasurement(models.Model):
    class Meta:
        verbose_name = "Единица измерения услуги"
        verbose_name_plural = "Единицы измерения услуг"

    title = models.CharField(verbose_name="Единица измерения", max_length=512)

    def __str__(self):
        return self.title


class ServicesList(models.Model):
    class Meta:
        verbose_name = "Перечень услуг"
        verbose_name_plural = "Перечни услуг"

    date_from = models.DateField(verbose_name="Действует от", default=datetime.datetime.now)
    date_to = models.DateField(verbose_name="Действителен до", null=True, blank=True)
    is_archived = models.BooleanField(verbose_name="В архиве",
                                      help_text="Для совместимости со старыми отчетами, "
                                                "установите флаг, вместо удаления услуги",
                                      default=False)

    def __str__(self):
        if self.date_to:
            return f"Перечень услуг от {self.date_from.strftime('%d.%m.%Y')} до {self.date_to.strftime('%d.%m.%Y')}"
        return f"Перечень услуг от {self.date_from.strftime('%d.%m.%Y')}"


class Service(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    PLACES = (
        ('H', 'на дому'),
        ('O', 'в организации (полустационар)'),
        ('-', 'повсеместно')
    )

    title = models.TextField(verbose_name="Наименование", max_length=512)
    type_of_service = models.CharField(verbose_name="Тип", choices=ServiceTypeEnum.choices,
                                       max_length=1, default=ServiceTypeEnum.PAID)
    service_category = models.CharField(verbose_name="Категория", choices=ServiceCategoryEnum.choices,
                                        max_length=2, default=None, null=True, blank=True)
    measurement = models.ForeignKey(to=ServiceMeasurement, on_delete=models.CASCADE,
                                    verbose_name="Единица измерения")
    tax = models.DecimalField(verbose_name="Стоимость", max_digits=6, decimal_places=2)  # max is 9999.99
    time_for_service = models.PositiveIntegerField(verbose_name="Количество рабочего времени (мин)",
                                                   blank=True, null=True)
    services_list = models.ForeignKey(to=ServicesList, on_delete=models.CASCADE, verbose_name="Перечень услуг")
    place = models.CharField(verbose_name="Место оказания", choices=PLACES, default='-', max_length=1)
    volume_limitation = models.ForeignKey(verbose_name="Ограничение объема", to=VolumeLimitation,
                                          default=get_one_volume, null=False, on_delete=models.SET_DEFAULT,
                                          help_text="Устаноивте значение если объем одной оказываемой услуги ограничен "
                                                    "(например 'не более 50 кв.м.')")
    period_limitation = models.ForeignKey(verbose_name="Ограничение периодичности", to=PeriodLimitation, default=None,
                                          null=True, on_delete=models.SET_NULL, blank=True,
                                          help_text="Установите значение если услуга ограничена периодичностью оказания"
                                                    " (например 'не более 2 раз в неделю'")
    objects = models.Manager()
    by_type = ServiceByTypeManger()

    def __str__(self):
        return f'{self.title}'
