import os

from django.db import models

from applications.social_work.services.models import Service
from utils.datetime import later_3_years
from .abstract import ContractBase
from ..enums import ContractTypeEnum


class IPPSU(ContractBase):
    class Meta:
        verbose_name = "ИППСУ"
        verbose_name_plural = "ИППСУ"

    __template_name__ = "ippsu.docx"
    __files_dir__ = os.path.join('contracts', 'ippsu')

    date_expiration = models.DateField(verbose_name="Действителен до", default=later_3_years)
    included_services = models.ManyToManyField(to=Service, verbose_name="Включенные услуги", blank=True)

    contract_type = ContractTypeEnum.IPPSU

    def get_current_journal(self):
        # TODO as queryset maybe
        import datetime
        now = datetime.datetime.now().date()
        # journal = self.provided_journals.filter(date_from__lte=now, date_from__gte=now)
        return self.provided_journals.filter(date_from__lte=now, date_to__gte=now).order_by('date_from',
                                                                                            'date_to').first()
