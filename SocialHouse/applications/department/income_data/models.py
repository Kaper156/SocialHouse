from django.db import models

# from applications.department.people.models.people import ServicedPerson
from utils.datetime import month_end


class LivingWage(models.Model):
    class Meta:
        verbose_name = "Прожиточный минимум"
        verbose_name_plural = "Прожиточный минимум"

    tax = models.DecimalField(verbose_name="Размер предельной величины среднедушевого дохода",
                              max_digits=9, decimal_places=2)
    date_to = models.DateField(verbose_name="По дате", default=month_end)

    def __str__(self):
        return f"[{self.date_to}] {self.tax}"


class AveragePerCapitaIncome(models.Model):
    class Meta:
        verbose_name = "Среднедушвые доходы за 12 месяцев"
        verbose_name_plural = "Среднедушвой доход за 12 месяцев"

    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to='people.ServicedPerson',
                                        blank=False, null=False, on_delete=models.CASCADE)
    date_to = models.DateField(verbose_name="По дате", default=month_end)
    avg_income = models.DecimalField(verbose_name="Среднедушевой доход за последние 12 месяцев",
                                     max_digits=9, decimal_places=2)

    def __str__(self):
        return f"[{self.date_to}] {self.serviced_person} - {self.avg_income}"


def last_living_wage():
    return LivingWage.objects.order_by('date_to').last()
