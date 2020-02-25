from datetime import datetime, timedelta


def later(delta: timedelta, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date + delta


def later_two_hours():
    return later(delta=timedelta(hours=2))


def later_years(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year + years)
    except ValueError:  # If february have 29 days
        return from_date.replace(month=2, day=28,
                                 year=from_date.year + years)


def later_3_years():
    return later_years(years=3)
