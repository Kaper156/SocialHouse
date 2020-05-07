from decimal import Decimal

from django.db import models

from applications.documents.models import DocumentDocx
from applications.people.models import ServicedPerson, WorkerPosition
from applications.social_work.providing.models import ProvidedServiceJournal
from applications.social_work.services.enums import ServiceTypeEnum


class Act(DocumentDocx):
    class Meta:
        abstract = True

    journal = models.ForeignKey(to=ProvidedServiceJournal, on_delete=models.CASCADE,
                                verbose_name="Журнал оказанных социальных услуг", related_name='%(class)s')
    additional_journal = models.ForeignKey(to=ProvidedServiceJournal, on_delete=models.CASCADE,
                                           verbose_name="Дополнительный журнал оказанных социальных услуг",
                                           related_name='%(class)s_additional', null=True, blank=True,
                                           help_text="Дополнительный журнал. Добавьте, "
                                                     "если ИППСУ заканчивается в середине месяца")

    def period(self):
        return self.journal.period()

    def get_aggregated_rows(self, type_of_service: ServiceTypeEnum):
        result_set = self.journal.get_aggregated_rows(type_of_service=type_of_service)
        if self.additional_journal:
            result_set.extend(self.additional_journal.get_aggregated_rows(type_of_service=type_of_service))
        return result_set

    def __get_serviced__(self) -> ServicedPerson:
        return self.journal.ippsu.serviced_person

    def __get_social_worker__(self) -> WorkerPosition:
        return self.journal.ippsu.social_worker

    def get_total_sum_for_rows(self, rows: list) -> Decimal:
        return sum(map(lambda row: row['total'], rows))

    def get_template_context(self):
        from django.utils import dateformat
        ctx = super().get_template_context()
        ctx['date1'] = self.journal.date_from
        ctx['date2'] = self.journal.date_to

        ctx['month'] = dateformat.format(self.journal.date_from, "F").lower()
        ctx['year'] = self.journal.date_from.year

        ctx['worker'] = self.__get_social_worker__().worker
        ctx['worker_position'] = self.__get_social_worker__().get_position_display()

        ctx['serviced'] = self.__get_serviced__()
        ctx['serviced_FIO'] = self.__get_serviced__().FIO()

        return ctx

    period.short_description = "Период"
