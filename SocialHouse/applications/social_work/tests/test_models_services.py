import datetime

from django.test import TestCase

from applications.core.enums import ServiceTypeEnum
from applications.social_work.enums import PeriodEnum, StatementEnum
from applications.social_work.models.ippsu import ProvidedService, ProvidedServiceJournal
from applications.social_work.models.services import Service, ServiceMeasurement, Statement, ServicesList


class ProvidedServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        # measurement = ServiceMeasurement(
        #     title="1,5 кв.м не более 2 раз в неделю",
        #     period=PeriodEnum.WEEK,
        #     period_statement=Statement(
        #         statement=StatementEnum.LESS_EQUAL,
        #         limit=2
        #     ),
        #     volume_statement=Statement(
        #         statement=StatementEnum.LESS_EQUAL,
        #         limit=1.5
        #     )
        # )
        #
        # service_list = ServicesList(
        #     date_from=datetime.date(2020, 1, 1),
        #     date_to=datetime.date(2020, 12, 31),
        # )
        #
        # service = Service.objects.create(
        #     title="Мытьё пола",
        #     type_of_service=ServiceTypeEnum.GUARANTEED,
        #     service_category=Service.SERVICE_CATEGORIES[0][0],
        #     measurement=measurement,
        #     tax=30.5,
        #     time_for_service=20,
        #     services_list=service_list,
        #     place=Service.PLACES[0][0]
        #
        # )
        # ippsu =
        # journal = ProvidedServiceJournal.objects.create(
        #
        # )
        # ProvidedService.objects.create(
        #     journal=journal,
        #     date_of=datetime.date(2020, 1, 31),
        #     service=service,
        #     # type_of_service=ServiceTypeEnum.GUARANTEED,
        #     volume=1.5,
        #     quantity=2
        # )
