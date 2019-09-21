from datetime import timedelta, datetime
from calendar import monthrange


def get_range_around_month(date=None):
    if date is None:
        date = datetime.now()
    d1, d2 = [datetime(date.year, date.month, d) for d in monthrange(date.year, date.month)]
    d2 += timedelta(hours=23, minutes=59, seconds=59)
    return d1, d2


def is_dates_in_one_month(date1: datetime, date2: datetime):
    return (date1.year == date2.year) & (date1.month == date2.month)


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


def load_services_from_csv(path_to_csv, delimiter=';', quotechar='\n', field_pairs=None):
    import csv
    if field_pairs is None:
        field_pairs = (
            ('title', 'title'),
            ('type_of_service', 'type_of_service'),
            ('service_category', 'service_category'),
            ('measurement', 'measurement'),
            ('tax', 'tax'),
            ('time_for_service', 'time_for_service'),
            ('is_archived', 'is_archived'),

        )
    with open(path_to_csv, 'rt') as f:
        csv_r = csv.reader(f, delimiter=delimiter, quotechar=quotechar)


def save_services_to_csv(path_to_csv, delimiter=';', quotechar='\n', field_pairs=None):
    from applications.social_work.models import Service, ServiceMeasurement
    import csv
    if field_pairs is None:
        field_pairs = (
            ('title', 'title'),
            ('type_of_service', 'type_of_service'),
            ('service_category', 'service_category'),
            ('measurement', 'measurement'),
            ('tax', 'tax'),
            ('time_for_service', 'time_for_service'),
            ('is_archived', 'is_archived'),

        )
    with open(path_to_csv, 'rt') as f:
        pass
