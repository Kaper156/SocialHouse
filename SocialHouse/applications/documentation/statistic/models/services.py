from django.db import models

from applications.documentation.acts.models import SocialAct, PaidAct
from applications.documentation.standardization.enums import DocumentPeriodTypeEnum
from utils.datetime import month_start, month_end


class StatisticServices(models.Model):
    class Meta:
        verbose_name = "Статистика по услугам"

    period_type = models.CharField(verbose_name="Период", choices=DocumentPeriodTypeEnum.choices,
                                   default=DocumentPeriodTypeEnum.MONTH, max_length=1)
    date_of_formation = models.DateField(verbose_name="Дата формирования статистики",
                                         help_text="Для формирования статистики за прошедший период, "
                                                   "выберите тип периода и дату внутри требуемого диапозона")

    acts_social = models.ManyToManyField(to=SocialAct, related_name="%(class)s", blank=True,
                                         verbose_name="Акты оказания социальных услуг",
                                         help_text="Можно оставить пустым, тогда система автоматически "
                                                   "соберет все акты за период")
    acts_paid = models.ManyToManyField(to=PaidAct, related_name="%(class)s", blank=True,
                                       verbose_name="Акты оказания платных услуг",
                                       help_text="Можно оставить пустым, тогда система автоматически "
                                                 "соберет все акты за период")
    date_from = models.DateField(verbose_name="Начало периода", default=month_start, editable=False)
    date_to = models.DateField(verbose_name="Конец периода", default=month_end, editable=False)

    # SUM
    sum_guaranteed = models.DecimalField(verbose_name="Сумма за оказание гарантированных услуг", max_digits=12,
                                         decimal_places=2, editable=False, default=0)
    sum_additional = models.DecimalField(verbose_name="Сумма за оказание дополнительных услуг", max_digits=12,
                                         decimal_places=2, editable=False, default=0)
    sum_paid = models.DecimalField(verbose_name="Сумма за оказание платных услуг", max_digits=12, decimal_places=2,
                                   editable=False, default=0)
    sum_social = models.DecimalField(verbose_name="Сумма за оказание гарантированных и дополнительных услуг",
                                     max_digits=12, decimal_places=2, editable=False, default=0)
    sum_total = models.DecimalField(verbose_name="Сумма за все оказанные услуги", max_digits=12, decimal_places=2,
                                    editable=False, default=0)
    # G and A

    # Quantity
    quantity_guaranteed = models.PositiveIntegerField(verbose_name="Количество оказанных гарантированных услуг",
                                                      editable=False, default=0)
    quantity_additional = models.PositiveIntegerField(verbose_name="Количество оказанных дополнительных услуг",
                                                      editable=False, default=0)
    quantity_paid = models.PositiveIntegerField(verbose_name="Количество оказанных платных услуг", editable=False,
                                                default=0)
    quantity_social = models.PositiveIntegerField(
        verbose_name="Количество оказанных гарантированных и дополнительных услуг", editable=False, default=0)
    quantity_total = models.PositiveIntegerField(verbose_name="Количество всех оказанных услуг", editable=False,
                                                 default=0)

    # TODO: def clean with auto load data by date
