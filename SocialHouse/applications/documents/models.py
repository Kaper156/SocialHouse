from applications.documents.utils.document import jinja_env
from datetime import datetime
import os
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import dateformat

from applications.core.models import LivingWage, AveragePerCapitaIncome
from applications.social_work.models import ProvidedServiceJournal
from docxtpl import DocxTemplate

fs = FileSystemStorage(location='/media/docs')


class Document(models.Model):
    class Meta:
        abstract = True

    __template_path__ = ''
    file = models.FileField(verbose_name="Файл", storage=fs, editable=False)

    def get_template_context(self):
        return {
            'kcson_chief': "руководитель БУ КЦСОН Тевризского района Берендеева Ольга Валиентиновна",
        }

    def get_templates_folder_path(self):
        if self.__template_path__:
            return self.__template_path__

        import applications.documents as docs_app
        self.__template_path__ = os.path.join(os.path.dirname(docs_app.__file__), 'templates', 'doc_templates')
        return self.__template_path__

    def get_template(self):
        raise Exception("Template not implemented now")

    def generate_doc(self):
        doc = DocxTemplate(self.get_template())
        context = self.get_template_context()
        doc.render(context, jinja_env=jinja_env)
        doc.save(self.file.path)
        return self.file.path


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
        ctx['serviced_FIO'] =  self.journal.ippsu.serviced_person.FIO()
        return ctx

    period.short_description = "Период"


def last_living_wage():
    return LivingWage.objects.order_by('date_to').last()


class SocialAct(Act):
    class Meta:
        abstract = False
        verbose_name = "Акты социальных услуг"
        verbose_name_plural = "Акт социальных услуг"

    living_wage = models.ForeignKey(verbose_name="Полтора прожиточных минимума для пенсионера",
                                    to=LivingWage, on_delete=models.CASCADE, null=False, blank=False,
                                    default=last_living_wage)

    avg_per_capita_income = models.ForeignKey(verbose_name="Средний душевой доход за 12 месяцев",
                                              to=AveragePerCapitaIncome, on_delete=models.CASCADE,
                                              null=False, blank=False)

    def get_template(self):
        return os.path.join(self.get_templates_folder_path(), 'act_social_services__v5.docx')

    def get_template_context(self):
        ctx = super().get_template_context()
        # ctx['']
        return ctx


class PaidAct(Act):
    class Meta:
        abstract = False
        verbose_name = "Акты платных услуг"
        verbose_name_plural = "Акт платных услуг"
