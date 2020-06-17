from django.db import models

from applications.department.events.models import Event
from applications.receptionist.meter.enums import MeterTypesEnum
from .abstract import ReportDocxBase, ReportXlsxBase
from ...standardization.enums import DocumentPeriodTypeEnum
from ...statistic.models import StatisticServices, SocialPassport, MeterStatistic


class DigitalYearReport(ReportXlsxBase):
    class Meta:
        verbose_name = "Ежегодный цифровой отчёт"
        verbose_name_plural = "Ежегодные цифровые отчёты"

    period_type = DocumentPeriodTypeEnum.YEAR
    social_passport = models.ForeignKey(SocialPassport, on_delete=models.PROTECT,
                                        verbose_name="На основании социального пасспорта",
                                        related_name="digital_year_reports", blank=True)

    service_total = models.ForeignKey(to=StatisticServices, verbose_name="На основании статистики услуг",
                                      on_delete=models.PROTECT,
                                      # limit_choices_to= # TODO: only year
                                      )
    # TODO link with digital-month


class CommonYearReport(ReportDocxBase):
    class Meta:
        verbose_name = "Ежегодный общий отчёт"
        verbose_name_plural = "Ежегодные общие отчёты"

    period_type = DocumentPeriodTypeEnum.YEAR

    digital_report = models.OneToOneField(DigitalYearReport, on_delete=models.PROTECT,
                                          verbose_name="На основании ежегодного цифрового отчёта",
                                          related_name="common_year_reports")
    events = models.ManyToManyField(to=Event, related_name="common_year_reports", verbose_name="События",
                                    help_text="Оставьте поле пустым, "
                                              "чтобы система автоматически добавила все события за год")


class MeterDataInfo(ReportDocxBase):
    class Meta:
        verbose_name = "Ежегодная информация о потреблении коммунальных услуг"

    period_type = DocumentPeriodTypeEnum.YEAR
    cold_water = models.ForeignKey(to=MeterStatistic, on_delete=models.CASCADE, verbose_name="Холодная вода",
                                   limit_choices_to={'meter_type': MeterTypesEnum.WATER_COLD}, null=True,
                                   related_name="df_cold_water")
    warm_water = models.ForeignKey(to=MeterStatistic, on_delete=models.CASCADE, verbose_name="Горячая вода",
                                   limit_choices_to={'meter_type': MeterTypesEnum.WATER_WARM}, null=True,
                                   related_name="df_warm_water")
    gasoline = models.ForeignKey(to=MeterStatistic, on_delete=models.CASCADE, verbose_name="Газоснабжение",
                                 limit_choices_to={'meter_type': MeterTypesEnum.GASOLINE}, null=True,
                                 related_name="df_gasoline")
    electricity = models.ForeignKey(to=MeterStatistic, on_delete=models.CASCADE, verbose_name="Электричество",
                                    limit_choices_to={'meter_type': MeterTypesEnum.ELECTRICITY}, null=True,
                                    related_name="df_electricity")
    heating = models.ForeignKey(to=MeterStatistic, on_delete=models.CASCADE, verbose_name="Отопление",
                                limit_choices_to={'meter_type': MeterTypesEnum.HEATING}, null=True,
                                related_name="df_heating")
