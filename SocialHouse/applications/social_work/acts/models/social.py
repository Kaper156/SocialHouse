import os

from django.db import models

from applications.serviced_data.models import LivingWage, AveragePerCapitaIncome, last_living_wage
from applications.social_work.acts.models.abstract import Act
from applications.social_work.services.enums import ServiceTypeEnum


class SocialAct(Act):
    class Meta:
        abstract = False
        verbose_name = "Акты социальных услуг"
        verbose_name_plural = "Акт социальных услуг"

    __template_name__ = "act_social.docx"
    __files_dir__ = os.path.join('acts', 'social_acts')

    living_wage = models.ForeignKey(verbose_name="Полтора прожиточных минимума для пенсионера",
                                    to=LivingWage, on_delete=models.CASCADE, null=False, blank=False,
                                    default=last_living_wage)

    avg_per_capita_income = models.ForeignKey(verbose_name="Средний душевой доход за 12 месяцев",
                                              to=AveragePerCapitaIncome, on_delete=models.CASCADE,
                                              null=False, blank=False)

    def get_file_name(self):
        ippsu = self.journal.ippsu
        return f"Акт_СУ {self.period()} {ippsu.serviced_person}.docx"

    def __prepare_context_for_guaranteed__(self, ctx: dict):
        ctx['guaranteed'] = self.get_aggregated_rows(ServiceTypeEnum.GUARANTEED)
        ctx['guaranteed'].extend(self.get_aggregated_rows(ServiceTypeEnum.CALCULATING))
        ctx['guaranteed_total'] = self.get_total_sum_for_rows(ctx['guaranteed'])

        ctx['living_wage_date'] = self.living_wage.date_to
        ctx['living_wage'] = self.living_wage.tax

        ctx['avg_per_capita_income'] = self.avg_per_capita_income.avg_income
        ctx['sale'] = (ctx['avg_per_capita_income'] - ctx['living_wage']) / 2
        if ctx['sale'] <= 0:
            ctx['sale'] = 0

        ctx['guaranteed_real_total'] = min(ctx['sale'], ctx['guaranteed_total'])
        ctx['sale'] = "Бесплатно по размеру дохода"
        return ctx

    def __prepare_context_for_additional__(self, ctx: dict):
        ctx['additional'] = self.get_aggregated_rows(ServiceTypeEnum.ADDITIONAL)
        ctx['additional_total'] = self.get_total_sum_for_rows(ctx['additional'])
        ctx['additional_real_total'] = ctx['additional_total']

        # TODO define as one-to-one? or relate with through
        privilege = self.__get_serviced__().privileges.first()
        ctx['privilege'] = privilege
        if ctx['privilege']:
            # Make 50% sale
            ctx['additional_real_total'] /= 2
        return ctx

    def get_template_context(self):
        import math
        ctx = super().get_template_context()
        ctx = self.__prepare_context_for_guaranteed__(ctx)
        ctx = self.__prepare_context_for_additional__(ctx)
        ctx['real_total'] = ctx['guaranteed_real_total'] + ctx['additional_real_total']
        ctx['real_total_rubles'] = math.floor(ctx['real_total'])
        ctx['real_total_kopeck'] = int((ctx['real_total'] - ctx['real_total_rubles']) * 100)

        return ctx

    def __str__(self):
        if self.additional_journal and self.journal.ippsu != self.additional_journal.ippsu:
            return f"{self.period()} ({self.journal.ippsu} + {self.additional_journal.ippsu})"
        return f"{self.period()} ({self.journal.ippsu})"
