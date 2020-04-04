from datetime import timedelta, datetime


def put_days_at_period(count, period: list):
    days = list()
    slots = (period[1] - period[0]).days + 1
    step = slots // count
    cur_date = period[0]
    while cur_date <= period[1]:
        days.append(cur_date)
        cur_date += timedelta(days=step)
    return days


class AssertProvidedServiceMixin:
    def assert_provided_service_eq(self, instance1, instance2):
        for key, value in instance1.__dict__.items():
            if not key.startswith('_') and key != 'id':
                self.assertEqual(instance2.__dict__[key], value)


if __name__ == '__main__':
    assert len(put_days_at_period(3, [datetime(2020, 1, 1), datetime(2020, 1, 3)])) == 3
    assert len(put_days_at_period(1, [datetime(2020, 1, 1), datetime(2020, 1, 3)])) == 1
    assert len(put_days_at_period(7, [datetime(2020, 1, 1), datetime(2020, 1, 14)])) == 7
