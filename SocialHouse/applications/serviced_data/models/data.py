from django.db import models
from django.urls import reverse

from applications.people.models.people import ServicedPerson


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
