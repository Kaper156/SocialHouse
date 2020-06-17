from utils.datetime import range_month, range_quarter, range_year
from ..standardization.enums import DocumentPeriodTypeEnum


def range_by_period_type(from_date, period_type: DocumentPeriodTypeEnum):
    if period_type.MONTH:
        return range_month(from_date)
    elif period_type.QUARTER:
        return range_quarter(from_date)
    elif period_type.YEAR:
        return range_year(from_date)
