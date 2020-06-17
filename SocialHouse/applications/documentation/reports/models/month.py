from django.db import models

from .abstract import ReportXlsxBase
from ...standardization.enums import DocumentPeriodTypeEnum
from ...statistic.models import SocialPassport, StatisticServices


class RegistryMonthly(ReportXlsxBase):
    class Meta:
        verbose_name = "Ежемесячный реестр оказания социальных услуг"
        verbose_name_plural = "Ежемесячные реестры оказания социальных услуг"

    period_type = DocumentPeriodTypeEnum.MONTH
    service_statistic = models.ForeignKey(to=StatisticServices, verbose_name="На основании статистики услуг",
                                          on_delete=models.PROTECT,
                                          limit_choices_to={'period_type': DocumentPeriodTypeEnum.MONTH})

    # TODO: get_template_context!


class DigitalMonthlyReport(ReportXlsxBase):
    class Meta:
        verbose_name = "Ежемесячный цифровой отчёт"
        verbose_name_plural = "Ежемесячные цифровые отчёты"

    period_type = DocumentPeriodTypeEnum.MONTH
    service_statistic = models.ForeignKey(to=StatisticServices, verbose_name="На основании статистики услуг",
                                          on_delete=models.PROTECT,
                                          limit_choices_to={'period_type': DocumentPeriodTypeEnum.MONTH})

    social_passport = models.ForeignKey(to=SocialPassport, on_delete=models.PROTECT,
                                        verbose_name="На основании социального пасспорта",
                                        related_name="digital_monthly_reports")

    previous_digital_report = models.ForeignKey(to='self', related_name="+", null=True, on_delete=models.PROTECT,
                                                verbose_name="Цифровой отчёт за прошлый месяц года",
                                                editable=True)

    # TODO: def clean with auto load/create social_passport by date
    # TODO check same dates of statistics
