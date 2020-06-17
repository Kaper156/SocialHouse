from applications.social_work.acts.models import SocialAct
from django.test import TestCase

from applications.social_work.services.enums import ServiceTypeEnum


class TestSocialAct(TestCase):
    fixtures = ['acts/tests/acts.json', ]

    @classmethod
    def setUpTestData(cls):
        cls.act = SocialAct.objects.first()

    def test_show_aggregated_rows(self):
        type_of_service = ServiceTypeEnum.PAID
        res = self.act.get_aggregated_rows(type_of_service)
        all_services = self.act.journal.services.filter(type_of_service=type_of_service)
        print(len(res))
        print(len(all_services))
        for service in res:
            print(service)
        max_q_service = max(res, key=lambda r: r['volume'])
        print()
        print()
        print(max_q_service)
        related_to_max_q_service = all_services.filter(service_id=max_q_service['service_id'])
        for r in related_to_max_q_service:
            print(r.__dict__)
            print(f"\t{r.service.__dict__}")

        # print()
        # print(self.first_service)
        # # print(res[self.first_service.title])
