from django.db import models
from django.urls import reverse

from applications.core.models.people import ServicedPerson
from applications.core.utils.datetime import month_end


class PassportData(models.Model):
    class Meta:
        verbose_name = "Пасспортные данные"
        verbose_name_plural = "Пасспортные данные"

    serial = models.CharField(max_length=4, verbose_name="Серия")
    number = models.CharField(max_length=6, verbose_name="Номер")
    date_of_issue = models.DateField(verbose_name="Дата выдачи")

    serviced_person = models.OneToOneField(ServicedPerson, on_delete=models.CASCADE,
                                           verbose_name="Обслуживаемый гражданин")

    def __str__(self):
        if self.serviced_person.gender == 'M':
            return f"Пасспорт гр-на {self.serviced_person}"
        else:
            return f"Пасспорт гр-ки {self.serviced_person}"

    def get_absolute_url(self):
        return reverse('passport_data_detail', args=[str(self.id)])


class Privilege(models.Model):
    class Meta:
        verbose_name = "Льготная категория"
        verbose_name_plural = "Льготные категории"

    title = models.TextField(max_length=1024, verbose_name="Название категории")

    def __str__(self):
        return self.title


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

    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to=ServicedPerson,
                                        blank=False, null=False, on_delete=models.CASCADE)
    date_to = models.DateField(verbose_name="По дате", default=month_end)
    avg_income = models.DecimalField(verbose_name="Среднедушевой доход за последние 12 месяцев",
                                     max_digits=9, decimal_places=2)

    def __str__(self):
        return f"[{self.date_to}] {self.serviced_person} - {self.avg_income}"