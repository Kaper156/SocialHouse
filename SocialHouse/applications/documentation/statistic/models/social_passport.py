from django.db import models

from applications.documentation.standardization.enums import DocumentPeriodTypeEnum
from utils.datetime import month_start, month_end


class SocialPassport(models.Model):
    class Meta:
        verbose_name = "Социальный паспорт"
        verbose_name_plural = "Социальные паспорта"

    period_type = models.CharField(verbose_name="Период", choices=DocumentPeriodTypeEnum.choices,
                                   default=DocumentPeriodTypeEnum.MONTH,
                                   max_length=1)
    date_of_formation = models.DateField(verbose_name="Дата формирования статистики",
                                         help_text="Для формирования статистики за прошедший период, "
                                                   "выберите тип периода и дату внутри требуемого диапозона")
    date_from = models.DateField(verbose_name="Начало периода", default=month_start, editable=False)
    date_to = models.DateField(verbose_name="Конец периода", default=month_end, editable=False)
    serviced_count = models.PositiveIntegerField(verbose_name="Количество получателей соц. услуг "
                                                              "на начало отчетного периода",
                                                 help_text="Оставьте пустым, "
                                                           "тогда система автоматически соберет данные за период")

    contracts_added = models.PositiveIntegerField(verbose_name="Заключено договоров",
                                                  help_text="Оставьте пустым, "
                                                            "тогда система автоматически соберет данные за период")
    contracts_stopped = models.PositiveIntegerField(verbose_name="Расторгнуто договоров",
                                                    help_text="Оставьте пустым, "
                                                              "тогда система автоматически соберет данные за период")

    serviced_moved_out = models.PositiveIntegerField(verbose_name="Переведено в другие отделения",
                                                     help_text="Оставьте пустым, "
                                                               "тогда система автоматически соберет данные за период")
    serviced_moved_in = models.PositiveIntegerField(verbose_name="Переведено из других отделений",
                                                    help_text="Оставьте пустым, "
                                                              "тогда система автоматически соберет данные за период")
    serviced_on_social_service = models.PositiveIntegerField(verbose_name="Состоит на обслуживании "
                                                                          "на конец отчетного периода",
                                                             help_text="Оставьте пустым, тогда система "
                                                                       "автоматически соберет данные за период")

    living_wage_less = models.PositiveIntegerField(verbose_name="Доход до 1,5 прожиточного минимума",
                                                   help_text="Оставьте пустым, тогда система "
                                                             "автоматически соберет данные за период")

    living_wage_more = models.PositiveIntegerField(verbose_name="Доход свыше 1,5 прожиточного минимума",
                                                   help_text="Оставьте пустым, тогда система "
                                                             "автоматически соберет данные за период")

    contracts_paused = models.PositiveIntegerField(verbose_name="Временно снятых с социального обслуживания",
                                                   help_text="Оставьте пустым, тогда система "
                                                             "автоматически соберет данные за период")

    contracts_returned = models.PositiveIntegerField(verbose_name="Восстановлено на обслуживание в течение месяца",
                                                     help_text="Оставьте пустым, тогда система "
                                                               "автоматически соберет данные за период")

    # TODO: def clean with auto load data by date
