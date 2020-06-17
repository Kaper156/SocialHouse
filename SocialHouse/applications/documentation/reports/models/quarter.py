from django.db import models

from applications.department.people_data.models import Privilege, default_privileges_for_additional
from .abstract import ReportDocxBase
from .month import RegistryMonthly
from ...standardization.enums import DocumentPeriodTypeEnum
from ...statistic.models import StatisticServices, SocialPassport


class QuarterActsBase(ReportDocxBase):
    class Meta:
        abstract = True

    # __template_name__ = ""

    period_type = DocumentPeriodTypeEnum.QUARTER
    service_total = models.ForeignKey(to=StatisticServices, verbose_name="На основании статистики",
                                      on_delete=models.PROTECT,
                                      # limit_choices_to= # TODO: only quarter
                                      )
    social_passport = models.ForeignKey(to=SocialPassport, on_delete=models.PROTECT,
                                        verbose_name="На основании социального пасспорта",
                                        related_name="%(class)s", blank=True)
    # TODO delete?
    monthly_registries = models.ManyToManyField(to=RegistryMonthly, related_name="%(class)s", null=True,
                                                verbose_name="Ежемесячные реестры оказания платных услуг",
                                                help_text="Можно оставить пустым, тогда система автоматически "
                                                          "соберет все реестры за период")

    # TODO: def clean with auto load acts


# АКТ оценки качества, эффективности и своевременности оказания услуг
class QuarterAct(QuarterActsBase):
    class Meta:
        verbose_name = "Ежеквартальный акт оценки качества"
        verbose_name_plural = "Ежеквартальные акты оценки качества"


class QuarterReportPrivileges(QuarterActsBase):
    class Meta:
        verbose_name = "Ежеквартальный акт оказанных дополнительных услуг ветеранам труда"
        verbose_name_plural = "Ежеквартальные акты оказанных дополнительных услуг ветеранам труда"

    privileges = models.ManyToManyField(to=Privilege, related_name="quarter_acts_privileges",
                                        verbose_name="Для категорий", default=default_privileges_for_additional)
