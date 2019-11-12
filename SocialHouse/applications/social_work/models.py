import datetime

from django.db import models

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
                                       blank=True, )
    # TODO check service_types_by_period


# TODO https://django-import-export.readthedocs.io/en/latest/getting_started.html#advanced-data-manipulation
# for serviceMeasurement use dehydrate newMeasure or existMeasure
# other links:
# https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
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
    )

    title = models.TextField(verbose_name="Наименование", max_length=512)
    type_of_service = models.CharField(verbose_name="Тип", choices=SERVICE_TYPES, max_length=1)
    service_category = models.CharField(verbose_name="Категория", choices=SERVICE_CATEGORIES,
                                        max_length=2)
    measurement = models.ForeignKey(to='ServiceMeasurement', on_delete=models.DO_NOTHING,
                                    verbose_name="Единица измерения (периодизация)")
    period = models.ForeignKey(to='ServicePeriod', on_delete=models.DO_NOTHING, verbose_name="Периодизация",
                               help_text="Оставьте пустым, если стоимость не зависит от переодичности",
                               null=True, blank=True)
    tax = models.DecimalField(verbose_name="Стоимость", max_digits=6, decimal_places=2)  # max is 9999.99
    time_for_service = models.PositiveIntegerField(verbose_name="Количество рабочего времени (мин)", blank=True)
    is_archived = models.BooleanField(verbose_name="В архиве",
                                      help_text="Для совместимости со старыми отчетами, "
                                                "установите флаг, вместо удаления услуги",
                                      default=False)

    def __str__(self):
        return f'{self.title}'


class ServicePeriod(models.Model):
    class Meta:
        verbose_name = "Периодизация услуги"
        verbose_name_plural = "Периодизации услуг"

    PERIODS = (
        ('D', "День"),
        ('W', "Неделю"),
        ('M', "Месяц"),
    )
    count = models.IntegerField(verbose_name="Количество", default=1)
    period = models.CharField(verbose_name="В срок", max_length=1,
                              choices=PERIODS)

    def __str__(self):
        return f'{self.count} единица в {self.get_period_display().lower()}'
    # TODO various signals for periods


class ServiceMeasurement(models.Model):
    class Meta:
        verbose_name = "Единица измерения услуги"
        verbose_name_plural = "Единицы измерения услуг"

    title = models.CharField(verbose_name="Единица измерения", max_length=128)
    short_title = models.CharField(verbose_name="Сокращенная запись", max_length=32, blank=True, null=True)

    def __str__(self):
        return self.short_title or self.title
