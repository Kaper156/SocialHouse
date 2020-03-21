import datetime

from django.db import models

from applications.social_work.statements.enums import PeriodEnum
from applications.social_work.statements.models import Statement, default_statement
from .enums import ServiceTypeEnum


class ServiceMeasurement(models.Model):
    class Meta:
        verbose_name = "Единица измерения услуги"
        verbose_name_plural = "Единицы измерения услуг"

    title = models.CharField(verbose_name="Единица измерения", max_length=512)

    period = models.IntegerField(verbose_name="В срок", choices=PeriodEnum.choices, null=True,
                                 help_text="Установите показатель, только если требуется ограничить услугу "
                                           "по частоте оказания (условие периодичности)")

    period_statement = models.ForeignKey(to=Statement, on_delete=models.SET_NULL, related_name='measurements_by_period',
                                         verbose_name="Условие периодичности", null=True, blank=True,
                                         help_text="Ограничевает оказание услуги по количеству (раз) в указанный период",
                                         default=default_statement)
    volume_statement = models.ForeignKey(to=Statement, on_delete=models.SET_NULL, related_name='measurements_by_volume',
                                         verbose_name="Условие превышения объема", null=True, blank=True,
                                         help_text="Ограничевает объем услуги",
                                         default=default_statement)

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

    SERVICE_CATEGORIES = (
        ('SB', "Социально-бытовые услуги"),
        ('ME', "Социально-медицинские услуги"),
        ('PS', "Социально-психологические услуги"),
        ('ED', "Социально-педагогические услуги"),
        ('WO', "Социально-трудовые услуги"),
        ('LA', "Социально-правовые услуги"),
        ('CO', "Услуги в целях повышения коммуникативного потенциала получателей социальных услуг "
               "имеющих ограничения жизнедеятельности, в том числе детей-инвалидов"),
        ('QU', "Срочные социальные услуги"),
        ('OT', "-Прочие"),
        ('UN', "Не указано"),
    )
    PLACES = (
        ('H', 'на дому'),
        ('O', 'в организации (полустационар)'),
        ('-', 'повсеместно')
    )

    title = models.TextField(verbose_name="Наименование", max_length=512)
    type_of_service = models.CharField(verbose_name="Тип", choices=ServiceTypeEnum.choices,
                                       max_length=1, default=ServiceTypeEnum.PAID)
    service_category = models.CharField(verbose_name="Категория", choices=SERVICE_CATEGORIES,
                                        max_length=2, default='UN')
    measurement = models.ForeignKey(to=ServiceMeasurement, on_delete=models.CASCADE,
                                    verbose_name="Единица измерения (периодизация)")
    tax = models.DecimalField(verbose_name="Стоимость", max_digits=6, decimal_places=2)  # max is 9999.99
    time_for_service = models.PositiveIntegerField(verbose_name="Количество рабочего времени (мин)",
                                                   blank=True, null=True)
    services_list = models.ForeignKey(to=ServicesList, on_delete=models.CASCADE, verbose_name="Перечень услуг")
    place = models.CharField(verbose_name="Место оказания", choices=PLACES, default='-', max_length=1)

    def __str__(self):
        return f'{self.title}'
