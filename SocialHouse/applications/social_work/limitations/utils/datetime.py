from applications.social_work.limitations.enums import PeriodEnum
from utils.datetime import range_week, range_month


def range_by_period_name(period_name, from_date=None):
    result_range = [None, None]
    if period_name == PeriodEnum.DAY:
        result_range = from_date, from_date
    if period_name == PeriodEnum.WEEK:
        result_range = range_week(from_date)
    if period_name == PeriodEnum.MONTH:
        result_range = range_month(from_date)
    return result_range
