from applications.social_work.statements.enums import PeriodEnum
from utils.datetime import range_week, range_month


def range_by_period_name(period_name, from_date=None):
    if period_name is PeriodEnum.DAY:
        return from_date, from_date
    if period_name is PeriodEnum.WEEK:
        return range_week(from_date)
    if period_name is PeriodEnum.MONTH:
        return range_month(from_date)
