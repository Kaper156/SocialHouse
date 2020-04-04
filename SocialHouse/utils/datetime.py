import calendar
import datetime


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


def random_date_between(date_from, date_to) -> datetime.date:
    from random import randint
    delta = date_to - date_from
    return date_from + datetime.timedelta(days=randint(0, delta.days))


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
    first_day = from_date - datetime.timedelta(days=from_date.weekday())
    last_day = first_day + datetime.timedelta(days=6)
    return first_day, last_day
