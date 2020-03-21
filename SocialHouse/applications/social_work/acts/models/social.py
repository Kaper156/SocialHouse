import os

from django.db import models

from applications.serviced_data.models import LivingWage, AveragePerCapitaIncome
from applications.social_work.acts.models.abstract import Act


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
