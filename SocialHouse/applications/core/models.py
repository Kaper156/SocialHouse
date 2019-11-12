import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.urls import reverse

# ONLY TWO.
GENDERS = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
)


class Worker(models.Model):
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    # TODO переделать описание
    STATUSES = (
        ('FI', "Уволен"),
        ('WO', "Работает"),
        ('ME', "На больничном"),
        ('VA', "В отпуске"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    name = models.CharField(max_length=128, blank=True, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=256, blank=True, verbose_name="Фамилия")

    gender = models.CharField(default='F', choices=GENDERS, max_length=1, verbose_name="Пол")

    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения",
                                     help_text="В формате ДД.ММ.ГГГГ (например 27.02.2019")

    status = models.CharField(max_length=2, choices=STATUSES, verbose_name="Статус", default='WO')

    def FIO(self, full=False):
        try:
            if not full:
                return f'{self.name[0]}.{self.patronymic[0]}. {self.surname}'
            return f'{self.name} {self.patronymic} {self.surname}'
        except self.DoesNotExist:
            return "Неизвестный работник"
        except IndexError:
            return "Неизвестный работник"

    def fullFIO(self):
        return self.FIO(full=True)

    def __str__(self):
        return self.FIO()

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Worker.objects.get(user=self.user)
                self.pk = p.pk
            except Worker.DoesNotExist:
                pass

        super(Worker, self).save(*args, **kwargs)


class Position(models.Model):
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    title = models.CharField(max_length=128, verbose_name="Название должности")
    purpose = models.TextField(max_length=1024, verbose_name="Назначение должности", blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа пользователей")

    def __str__(self):
        return f'{self.title}'


class WorkerPosition(models.Model):
    class Meta:
        verbose_name = "Ставка сотрудника"
        verbose_name_plural = "Ставки сотрудников"

    worker = models.ForeignKey('Worker', related_name='membership', on_delete=models.CASCADE, verbose_name="Сотрудник")
    position = models.ForeignKey('Position', related_name='membership', on_delete=models.CASCADE,
                                 verbose_name="Должность")
    date_of_appointment = models.DateField(verbose_name="Дата устройства на должность",
                                           default=datetime.datetime.now)
    dismissal_date = models.DateField(verbose_name="Дата увольнения с должности", null=True, blank=True)
    rate = models.FloatField(verbose_name="Ставка", default=1)

    def __str__(self):
        return f'{self.worker} ({self.position}) [x{self.rate}]'


class ServicedPerson(models.Model):
    class Meta:
        verbose_name = "Обслуживаемый"
        verbose_name_plural = "Обслуживаемые"

    LOCATIONS = (
        ('HE', "На обслуживании"),
        ('ME', "На лечении"),
        ('OU', "В поездке"),
    )

    name = models.CharField(max_length=128, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=256, verbose_name="Фамилия")

    gender = models.CharField(default='M', choices=GENDERS, max_length=1, verbose_name="Пол")
    date_of_birth = models.DateField(null=True, verbose_name="Дата рождения",
                                     help_text="В формате ДД.ММ.ГГГГ (например 27.02.2019")
    location = models.CharField(choices=LOCATIONS, max_length=2, verbose_name="Местонахождение", default="HE")

    privilege = models.ForeignKey('Privilege', on_delete=models.SET_NULL, verbose_name="Льготная категория", null=True)

    date_of_death = models.DateField(null=True, blank=True, verbose_name="Дата смерти")
    date_of_departure = models.DateField(null=True, blank=True, verbose_name="Дата ухода")

    def FIO(self, full=False):
        if not full:
            return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"
        return f"{self.name} {self.patronymic} {self.surname}"

    def get_absolute_url(self):
        return reverse('serviced_person_detail', args=[str(self.id)])

    def __str__(self):
        return self.FIO()


class Privilege(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название категории")


# Keep minimal needed info from passport to perform data in documents
class PassportData(models.Model):
    class Meta:
        verbose_name = "Пасспортные данные"

    serial = models.CharField(max_length=4, verbose_name="Серия")
    number = models.CharField(max_length=6, verbose_name="Номер")
    date_of_issue = models.DateField(verbose_name="Дата выдачи")

    serviced_person = models.OneToOneField('ServicedPerson', on_delete=models.CASCADE,
                                           verbose_name="Обслуживаемый гражданин")

    def __str__(self):
        if self.serviced_person.gender == 'M':
            return f"Пасспорт гр-на {self.serviced_person}"
        else:
            return f"Пасспорт гр-ки {self.serviced_person}"

    def get_absolute_url(self):
        return reverse('passport_data_detail', args=[str(self.id)])
