from django.db import models

from .abstract import Act


class PaidAct(Act):
    class Meta:
        verbose_name = "Акты оказания платных услуг"
        verbose_name_plural = "Акт оказания платных услуг"

    sum_paid = models.DecimalField(verbose_name="Сумма за оказание платных услуг", max_digits=12, decimal_places=2,
                                   editable=False, default=0)
    quantity_paid = models.PositiveIntegerField(verbose_name="Количество оказанных платных услуг", editable=False,
                                                default=0)
