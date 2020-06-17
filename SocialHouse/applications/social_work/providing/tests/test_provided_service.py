import datetime

from applications.social_work.contracts.exceptions import ServiceNotIncluded
from django.test import TestCase

from applications.social_work.limitations.models import VolumeLimitation, PeriodLimitation
from applications.social_work.providing.models import ProvidedService, ProvidedJournal
from applications.social_work.services.enums import ServiceTypeEnum
from applications.social_work.services.models import Service, ServiceMeasurement, ServicesList


class TestGuaranteedProvidedService(TestCase):
    service_name = 'Тестовая услуга'
    fixtures = ['providing/tests/providing.json', ]

    def setUp(self) -> None:
        # Only for debugging
        def str_for_provided(self: ProvidedService):
            return f"{self.volume} * {self.quantity}"

        ProvidedService.__str__ = str_for_provided

    def test_guaranteed_service__not_included_in_ippsu(self):
        # Make new service
        service = Service.objects.create(title=self.service_name,
                                         measurement=ServiceMeasurement.objects.first(),
                                         type_of_service=ServiceTypeEnum.GUARANTEED,
                                         tax=1,
                                         time_for_service=1,
                                         services_list=ServicesList.objects.first(),
                                         volume_limitation=VolumeLimitation.objects.first(),
                                         period_limitation=PeriodLimitation.objects.first(),
                                         )
        date = datetime.datetime.now()
        journal = ProvidedJournal.objects.first()
        # Set it to new provided service
        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=25,
            quantity=1,
            journal=journal,
        )
        with self.assertRaises(ServiceNotIncluded):
            provided_service.save()

    def test_guaranteed_service__split_by_volume(self):
        service = Service.objects.filter(title=self.service_name,
                                         volume_limitation__limit=10,
                                         type_of_service=ServiceTypeEnum.GUARANTEED
                                         ).first()
        date = datetime.datetime.now()
        journal = ProvidedJournal.objects.first()
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=5.0,
                quantity=1,
                journal=journal,
            ),
        ]
        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=25,
            quantity=1,
            journal=journal,
        )
        provided_service.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-volume')
        for index, actual_service in enumerate(actual.all()):
            self.assertEqual(actual_service.volume, expected[index].volume)
            self.assertEqual(actual_service.quantity, expected[index].quantity)

    def test_guaranteed_service__split_by_quantity__correct_period(self):
        service = Service.objects.filter(title=self.service_name,
                                         volume_limitation__limit=10,
                                         type_of_service=ServiceTypeEnum.GUARANTEED
                                         ).first()
        date = datetime.datetime.now()
        journal = ProvidedJournal.objects.first()
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),
        ]
        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=10,
            quantity=2,
            journal=journal,
        )
        provided_service.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-volume')
        for index, actual_service in enumerate(actual.all()):
            self.assertEqual(actual_service.volume, expected[index].volume)
            self.assertEqual(actual_service.quantity, expected[index].quantity)

    def test_guaranteed_service__split_by_quantity_and_volume__correct_period(self):
        service = Service.objects.filter(title=self.service_name,
                                         volume_limitation__limit=10,
                                         type_of_service=ServiceTypeEnum.GUARANTEED
                                         ).first()
        date = datetime.datetime.now()
        journal = ProvidedJournal.objects.first()
        expected = [
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),
            ProvidedService(
                date_of=date,
                service=service,
                volume=10.0,
                quantity=1,
                journal=journal,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=5.0,
                quantity=1,
                journal=journal,
            ),

            ProvidedService(
                date_of=date,
                service=service,
                volume=5.0,
                quantity=1,
                journal=journal,
            ),
        ]
        provided_service = ProvidedService(
            date_of=date,
            service=service,
            volume=15,
            quantity=2,
            journal=journal,
        )
        provided_service.save()

        actual = ProvidedService.objects.filter(journal=journal).order_by('-volume')
        for index, actual_service in enumerate(actual.all()):
            self.assertEqual(actual_service.volume, expected[index].volume)
            self.assertEqual(actual_service.quantity, expected[index].quantity)
