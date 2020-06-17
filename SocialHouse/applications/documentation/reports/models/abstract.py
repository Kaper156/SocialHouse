import datetime

from django.db import models

from ..utils import range_by_period_type
from ...standardization.enums import DocumentPeriodTypeEnum
from ...standardization.models import DocumentDocx, DocumentXlsx


class PeriodicMixin:
    def __set_self_period__(self, by_previous_month_auto=True):
        df = self.date_of_formation = datetime.date
        if by_previous_month_auto:
            # Set on previous month
            df = datetime.date(df.year, df.month, 1) - datetime.timedelta(days=1)

        # Set them by period range
        self.period_from, self.period_to = range_by_period_type(df, self.period_type)

    def period(self):
        from django.utils import dateformat
        # TODO for quarter and year
        period = dateformat.format(self.date_of_formation, "F Y").lower()
        return f"{self._meta.verbose_name} за {period}"

    period.description = "Период"

    def __str__(self):
        return self.period()


class ReportDocxBase(DocumentDocx, PeriodicMixin):
    class Meta:
        abstract = True

    date_of_formation = models.DateField(verbose_name="Дата формирования", default=datetime.datetime.now)

    period_type = DocumentPeriodTypeEnum.MONTH

    period_from = models.DateField(verbose_name="Начало периода",
                                   help_text="Если оставить пустым будет выбран "
                                             "период предшествующий выбранной дате формирования")
    period_to = models.DateField(verbose_name="Конец периода",
                                 help_text="Если оставить пустым будет выбран "
                                           "период предшествующий выбранной дате формирования")


class ReportXlsxBase(DocumentXlsx, PeriodicMixin):
    class Meta:
        abstract = True

    date_of_formation = models.DateField(verbose_name="Дата формирования", default=datetime.datetime.now)

    period_type = DocumentPeriodTypeEnum.MONTH

    period_from = models.DateField(verbose_name="Начало периода",
                                   help_text="Если оставить пустым будет выбран "
                                             "период предшествующий выбранной дате формирования")
    period_to = models.DateField(verbose_name="Конец периода",
                                 help_text="Если оставить пустым будет выбран "
                                           "период предшествующий выбранной дате формирования")
