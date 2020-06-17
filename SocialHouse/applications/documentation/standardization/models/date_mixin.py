import datetime

from django.db import models

from .docx import DocumentDocx
from .excel import DocumentXlsx
from ..enums import DocumentPeriodTypeEnum


class MixinWithDatePeriod:
    # Default Month
    date_type = DocumentPeriodTypeEnum.MONTH

    def __get_self_period__(self):
        from_date = self.date_of_formation
        # TODO if date in the begging of month - set previous range
        # else in current
        raise NotImplementedError


class DocxWithDateRange(DocumentDocx, MixinWithDatePeriod):
    class Meta:
        abstract = True

    date_of_formation = models.DateField(verbose_name="Дата формирования", default=datetime.datetime.now)


class XlsxWithDateRange(DocumentXlsx, MixinWithDatePeriod):
    class Meta:
        abstract = True

    date_of_formation = models.DateField(verbose_name="Дата формирования", default=datetime.datetime.now)
