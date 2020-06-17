import datetime

from django.test import TestCase

from applications.social_work.limitations.enums import PeriodEnum
from applications.social_work.providing.models import ProvidedService, ProvidedJournal
from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service
from utils.datetime import range_month
from .helpers import put_days_at_period, AssertProvidedServiceMixin


class TestGuaranteedProvidedService(TestCase, AssertProvidedServiceMixin):
    service_name = 'Тестовая услуга'
    fixtures = ['providing/tests/providing.json', ]

    # Set __str__ for provided service
    def setUp(self) -> None:
        def pstr(self: ProvidedService):
            return f"{self.date_of}" \
                   f"|{self.volume}({self.service.volume_limitation.limit})" \
                   f"/{self.quantity}({self.service.period_limitation.limit})" \
                   f"|{self.get_type_of_service_display()}"

        ProvidedService.__str__ = pstr

    @classmethod
    def setUpTestData(cls):
        cls.service_g_month_3 = Service.objects.filter(title=cls.service_name,
                                                       period_limitation__limit=3,
                                                       period_limitation__period=PeriodEnum.MONTH,
                                                       type_of_service=ServiceTypeEnum.GUARANTEED
                                                       ).first()
        cls.service_g_week_2 = Service.objects.filter(title=cls.service_name,
                                                      period_limitation__limit=2,
                                                      period_limitation__period=PeriodEnum.WEEK,
                                                      type_of_service=ServiceTypeEnum.GUARANTEED
                                                      ).first()
        cls.service_g_day_1 = Service.objects.filter(title=cls.service_name,
                                                     period_limitation__limit=1,
                                                     period_limitation__period=PeriodEnum.DAY,
                                                     type_of_service=ServiceTypeEnum.GUARANTEED
                                                     ).first()
        cls.journal = ProvidedJournal.objects.first()

    def test_journal__with_one_guaranteed_service__period_over_limit_by_month(self):
        service = self.service_g_month_3
        date = datetime.datetime.now()
        journal = self.journal
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=1,
            quantity=5,
            journal=journal,
        )
        provided_service.save()
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-type_of_service')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_journal__with_one_guaranteed_service__period_over_limit_by_week_in_middle_of_month(self):
        service = self.service_g_week_2
        date = datetime.datetime(year=2020, month=2, day=8)
        journal = self.journal
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=1,
            quantity=4,
            journal=journal,
        )
        provided_service.save()
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-type_of_service')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_journal__with_one_guaranteed_service__period_over_limit_by_day(self):
        service = self.service_g_day_1
        date = datetime.datetime.now()
        journal = self.journal
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=1,
            quantity=3,
            journal=journal,
        )
        provided_service.save()
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-type_of_service')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_journal__with_5_guaranteed_service__period_over_limit_by_month(self):
        service = self.service_g_month_3
        date1, date2 = datetime.datetime(year=2020, month=1, day=1), datetime.datetime(year=2020, month=1, day=31)
        days = put_days_at_period(5, [date1, date2])

        journal = self.journal
        expected = [
            ProvidedService(
                date_of=days[0],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=days[1],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=days[2],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=days[3],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),

            ProvidedService(
                date_of=days[4],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_services = [
            ProvidedService(
                date_of=days[0],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[1],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[2],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[3],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[4],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),

        ]

        list(map(lambda ps: ps.save(), provided_services))
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('date_of')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_journal__with_3_guaranteed_service__period_over_limit_by_week_in_middle_of_month(self):
        service = self.service_g_week_2
        # date = datetime.datetime(year=2020, month=2, day=8)
        date1, date2 = datetime.datetime(year=2020, month=1, day=6), datetime.datetime(year=2020, month=1, day=12)
        days = put_days_at_period(3, [date1, date2])
        journal = self.journal
        expected = [
            ProvidedService(
                date_of=days[0],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=days[1],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=days[2],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_services = [
            ProvidedService(
                date_of=days[0],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[1],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=days[2],
                service=service,
                volume=1,
                quantity=1,
                journal=journal,
            ),

        ]

        list(map(lambda ps: ps.save(), provided_services))
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('date_of')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_journal__with_3_guaranteed_by_day_and_4_by_month_over_limit(self):
        service_month = self.service_g_month_3
        service_day = self.service_g_day_1
        date1 = datetime.datetime(year=2020, month=1, day=5)
        date2 = datetime.datetime(year=2020, month=1, day=15)

        journal = self.journal
        expected = [
            ProvidedService(
                date_of=date1,
                service=service_day,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date1,
                service=service_day,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
            ProvidedService(
                date_of=date2,
                service=service_day,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),

            ProvidedService(
                date_of=date1,
                service=service_month,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date1,
                service=service_month,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date2,
                service=service_month,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date2,
                service=service_month,
                volume=1,
                quantity=1,
                journal=journal,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),

        ]

        provided_services = [
            ProvidedService(
                date_of=date1,
                service=service_day,
                volume=1,
                quantity=2,
                journal=journal,
            ),
            ProvidedService(
                date_of=date2,
                service=service_day,
                volume=1,
                quantity=1,
                journal=journal,
            ),

            ProvidedService(
                date_of=date1,
                service=service_month,
                volume=1,
                quantity=2,
                journal=journal,
            ),

            ProvidedService(
                date_of=date2,
                service=service_month,
                volume=1,
                quantity=2,
                journal=journal,
            ),
        ]
        list(map(lambda ps: ps.save(), provided_services))
        journal.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('service', 'date_of', '-type_of_service', )
        print(actual.filter(service=service_month).values())
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])

    def test_2_journal__with_4_guaranteed_by_week_in_start_over_limit(self):
        service = self.service_g_week_2
        # date = datetime.datetime(year=2020, month=2, day=8)
        date1, date2 = datetime.datetime(year=2020, month=1, day=31), datetime.datetime(year=2020, month=2, day=1)
        journal_old = self.journal
        new_journal_month_range = range_month(date2)
        journal_new = ProvidedJournal(
            ippsu=journal_old.ippsu,
            date_from=new_journal_month_range[0],
            date_to=new_journal_month_range[1],
        )
        journal_new.save()

        expected = [
            # Services in old journal must be GUARANTEED
            ProvidedService(
                date_of=date1,
                service=service,
                volume=1,
                quantity=1,
                journal=journal_old,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            ProvidedService(
                date_of=date1,
                service=service,
                volume=1,
                quantity=1,
                journal=journal_old,
                type_of_service=ServiceTypeEnum.GUARANTEED,
            ),
            # Services in new journal must be PAID_FROM_GUARANTEED
            ProvidedService(
                date_of=date2,
                service=service,
                volume=1,
                quantity=1,
                journal=journal_new,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
            ProvidedService(
                date_of=date2,
                service=service,
                volume=1,
                quantity=1,
                journal=journal_new,
                type_of_service=ServiceTypeEnum.PAID_FROM_GUARANTEED,
            ),
        ]

        provided_services = [
            ProvidedService(
                date_of=date1,
                service=service,
                volume=1,
                quantity=2,
                journal=journal_old,
            ),
            ProvidedService(
                date_of=date2,
                service=service,
                volume=1,
                quantity=1,
                journal=journal_new,
            ),
        ]

        list(map(lambda ps: ps.save(), provided_services))
        journal_old.save()
        journal_new.save()

        actual = ProvidedService.objects.filter(journal__ippsu=journal_old.ippsu).order_by('date_of')
        for index, actual_service in enumerate(actual.all()):
            self.assert_provided_service_eq(actual_service, expected[index])
