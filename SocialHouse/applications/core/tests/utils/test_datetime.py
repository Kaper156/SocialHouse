import datetime
from unittest import TestCase

from applications.core.utils.datetime import range_month, range_week


class TestRangeFunctions(TestCase):
    def test_range_week_in_middle_of_month(self):
        date = datetime.date(2020, 1, 15)
        expected_range = (datetime.date(2020, 1, 13),
                          datetime.date(2020, 1, 19))
        actual_range = range_week(date)
        self.assertSequenceEqual(expected_range, actual_range)

    def test_range_week_between_two_months(self):
        date = datetime.date(2020, 5, 1)
        expected_range = (datetime.date(2020, 4, 27),
                          datetime.date(2020, 5, 3))
        actual_range = range_week(date)
        self.assertSequenceEqual(expected_range, actual_range)

    def test_range_month_february_29(self):
        date = datetime.date(2020, 2, 15)
        expected_range = (datetime.date(2020, 2, 1),
                          datetime.date(2020, 2, 29))
        actual_range = range_month(date)
        self.assertSequenceEqual(expected_range, actual_range)
