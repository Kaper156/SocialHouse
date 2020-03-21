from django.db import models

from applications.documents.models import Document
from applications.social_work.providing.models import ProvidedServiceJournal


class Act(Document):
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

    def get_template_context(self):
        from django.utils import dateformat
        ctx = super().get_template_context()
        ctx['date1'] = self.journal.date_from
        ctx['date2'] = self.journal.date_to
        ctx['month'] = dateformat.format(self.journal.date_from, "F").lower()
        ctx['year'] = self.journal.date_from.year

        ctx['worker'] = self.journal.ippsu.social_worker.worker
        ctx['serviced'] = self.journal.ippsu.serviced_person
        ctx['serviced_FIO'] = self.journal.ippsu.serviced_person.FIO()
        return ctx

    period.short_description = "Период"
