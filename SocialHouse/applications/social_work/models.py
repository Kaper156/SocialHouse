from django.db import models
# from applications.core.models import ServicedPerson, WorkerPosition

import datetime

SERVICE_TYPES = (
    ('G', "Гарантированная"),
    ('A', "Дополнительная"),
    ('P', "Платная"),
)


class ServiceJournal(models.Model):
    class Meta:
        verbose_name = "Оказанная услуга"
        verbose_name_plural = "Оказанные услуги"

    date_of = models.DateTimeField(verbose_name="Дата оказания", default=datetime.datetime.now)
    serviced = models.ForeignKey(to='core.ServicedPerson', on_delete=models.CASCADE,
                                 verbose_name="Обслуживаемый")
    employer = models.ForeignKey(to='core.WorkerPosition', on_delete=models.CASCADE,
                                 verbose_name="Социальный работник")
    service = models.ForeignKey(to='Service', on_delete=models.CASCADE, verbose_name="Услуга")

    # TODO form https://stackoverflow.com/questions/6862250/change-a-django-form-field-to-a-hidden-field
    type_of_service = models.CharField(verbose_name="Тип услуги", choices=SERVICE_TYPES, max_length=1,
                                       blank=True)
    # TODO check service_types_by_period


class Service(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    # TODO добавить категории с "-"
    SERVICE_CATEGORIES = (
        ('SB', "Социальная"),
        ('PS', "Психологическая"),
        ('OT', "-Прочие"),
    )
    title = models.TextField(verbose_name="Название", max_length=512)
    service_category = models.CharField(verbose_name="Категория", choices=SERVICE_CATEGORIES,
                                        max_length=2)
    period = models.ForeignKey(to='Period', on_delete=models.CASCADE,
                               verbose_name="Периодизация", null=True)
    type_of_service = models.CharField(verbose_name="Тип", choices=SERVICE_TYPES, max_length=1)


class ServiceTariff(models.Model):
    class Meta:
        verbose_name = "Тариф услуги"
        verbose_name_plural = "Тарифы услуг"

    service = models.ForeignKey(to='Service', on_delete=models.CASCADE, verbose_name="Услуга")
    tax = models.DecimalField(verbose_name="Стоимость", decimal_places=2, max_digits=92)
    date_in = models.DateTimeField(verbose_name="Действие тарифа от", default=datetime.datetime.now)
    date_out = models.DateTimeField(verbose_name="Действие тарифа до", null=True,
                                    help_text="Можно оставить пустым, если тариф действует до сих пор")


# TODO LATER
class Period(models.Model):
    class Meta:
        verbose_name = "Периодизация услуги"
        verbose_name_plural = "Периодизация услуг"

    PERIODS = (
        # ('D', "День"),
        ('W', "Неделя"),
        ('M', "Месяц"),
        ('H', "Полугодие"),
        ('Y', "Год"),
    )
    period = models.CharField(verbose_name="Тип периода", max_length=1, choices=PERIODS)
    count = models.IntegerField(verbose_name="Количество", default=1)
