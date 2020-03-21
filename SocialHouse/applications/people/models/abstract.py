from django.db import models
from django.utils import dateformat

from utils.datetime import month_start, month_end

GENDERS = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)


class Person(models.Model):
    class Meta:
        abstract = True
        ordering = ['surname', 'name', 'patronymic']

    name = models.CharField(max_length=128, blank=False, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=False, verbose_name="Отчество")
    surname = models.CharField(max_length=256, blank=False, verbose_name="Фамилия")

    def FIO(self, full=False):
        if full:
            return f'{self.name} {self.patronymic} {self.surname}'
        return f'{self.surname} {self.name[0]}.{self.patronymic[0]}.'

    def fullFIO(self):
        return self.FIO(full=True)

    FIO.short_description = "Ф.И.О."

    def __str__(self):
        return self.fullFIO()


class ExtendedPerson(Person):
    class Meta:
        abstract = True

    gender = models.CharField(default='F', choices=GENDERS, max_length=1, verbose_name="Пол")
    date_of_birth = models.DateField(null=False, blank=False, verbose_name="Дата рождения",
                                     help_text="В формате ДД.ММ.ГГГГ (например 27.02.2019")


# TODO: delete (unused)
class Journal(models.Model):
    class Meta:
        abstract = True

    date_from = models.DateField(verbose_name="Период от", default=month_start)
    date_to = models.DateField(verbose_name="Период до", default=month_end)

    def period(self):
        return dateformat.format(self.date_from, 'Y-m F')

    period.short_description = "Период"
