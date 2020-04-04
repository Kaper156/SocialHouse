from django.db import models

from .enums import PeriodEnum


class VolumeLimitation(models.Model):
    class Meta:
        verbose_name = "Условие ограничения объема предоставления услуги"
        verbose_name_plural = "Условия ограничения объема предоставления услуг"

    limit = models.FloatField(verbose_name="Ограничение", default=1, unique=True,
                              help_text="Укажите ограничение (к примеру не более 1 (кв.м) или не более двух (изделий)")

    def __str__(self):
        return f"Не более {self.limit} единиц измерения"


def get_one_volume():
    return VolumeLimitation.objects.get_or_create(
        limit=1.0
    )[0]


class PeriodLimitation(models.Model):
    class Meta:
        verbose_name = "Условие ограничения периодичности предоставления услуги"
        verbose_name_plural = "Условия ограничения периодичности предоставления услуг"

    period = models.IntegerField(verbose_name="Периодичность", choices=PeriodEnum.choices, default=PeriodEnum.MONTH)
    limit = models.IntegerField(verbose_name="Ограничение", default=1, help_text="Укажите ограничение "
                                                                                 "(к примеру не более одного "
                                                                                 "или не более двух")

    def __str__(self):
        res = f"{self.limit} раз в {self.get_period_display()}"
        if self.limit == 1:
            return "Ровно " + res
        return "Не более " + res
