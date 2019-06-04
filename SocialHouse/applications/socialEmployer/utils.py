from datetime import timedelta, datetime


def get_date_range_around(date_in, p_type):
    date_in = datetime(date_in.year, date_in.month, date_in.day)
    bef = aft = date_in

    if p_type == 'W':
        bef = date_in - timedelta(days=date_in.weekday())
        aft = bef + timedelta(days=6)
    elif p_type == 'M':
        bef = date_in - timedelta(days=date_in.day - 1)
        aft = bef + timedelta(days=30)
    # TODO сверку количества дней в месяце
    # TODO год

    aft = aft + timedelta(hours=23, minutes=59, seconds=59)

    return bef, aft
