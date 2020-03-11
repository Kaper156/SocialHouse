import datetime
import calendar

from applications.social_work.enums import PeriodEnum


def def_date() -> datetime.date:
    return datetime.datetime.now().date()


def later(delta: datetime.timedelta, from_date=None):
    from_date = from_date or def_date()
    return from_date + delta


def later_two_hours():
    return later(delta=datetime.timedelta(hours=2))


def later_years(years, from_date=None):
    from_date = from_date or def_date()
    try:
        return from_date.replace(year=from_date.year + years)
    except ValueError:  # If february have 29 days
        return from_date.replace(month=2, day=28,
                                 year=from_date.year + years)


def later_3_years():
    return later_years(years=3)


def month_start(from_date=None):
    from_date = from_date or def_date()
    return from_date.replace(day=1)


def month_end(from_date=None):
    from_date = from_date or def_date()
    last_day = calendar.monthrange(from_date.year, from_date.month)[1]
    return from_date.replace(day=last_day)


def range_month(from_date=None):
    from_date = from_date or def_date()
    return (
        datetime.date(from_date.year, from_date.month, 1),
        datetime.date(from_date.year, from_date.month, calendar.monthrange(from_date.year, from_date.month)[1])
    )


def range_week(from_date=None):
    from_date = from_date or def_date()
    first_day = calendar.weekday(from_date.year, from_date.month, from_date.day)
    last_day = first_day + datetime.timedelta(days=7)
    return first_day, last_day


def range_by_period_name(period_name, from_date=None):
    if period_name is PeriodEnum.DAY:
        return from_date, from_date
    if period_name is PeriodEnum.WEEK:
        return range_week(from_date)
    if period_name is PeriodEnum.MONTH:
        return range_month(from_date)
