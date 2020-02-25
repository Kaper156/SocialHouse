import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.urls import reverse

# ONLY TWO.
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


class Worker(ExtendedPerson):
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    STATUSES = (
        ('FI', "Уволен"),
        ('WO', "Работает"),
        ('ME', "На больничном"),
        ('VA', "В отпуске"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=2, choices=STATUSES, verbose_name="Статус", default='WO')

    def get_positions(self):
        return '; '.join(wp.position.title for wp in self.membership.all())

    get_positions.short_description = "Занимаемые должности"

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


class ServicedPerson(ExtendedPerson):
    class Meta:
        verbose_name = "Обслуживаемый"
        verbose_name_plural = "Обслуживаемые"

    STATUSES = (
        ('HE', "На обслуживании"),
        ('ME', "На лечении"),
        ('OU', "В поездке"),
        ('LE', "Покинул отделение"),
        ('DE', "Умерший"),
    )
    location = models.CharField(choices=STATUSES, max_length=2, verbose_name="Местонахождение", default="HE")

    privileges = models.ManyToManyField(to='Privilege', verbose_name='Льготные категории', blank=True)

    date_of_death = models.DateField(null=True, blank=True, verbose_name="Дата смерти")
    date_of_departure = models.DateField(null=True, blank=True, verbose_name="Дата ухода")

    def privileges_in_str(self):
        if not self.privileges.exists():
            return 'Без льгот'
        return '; '.join(p.title for p in self.privileges.all())

    def is_dead(self):
        return self.date_of_death and self.date_of_death < datetime.datetime.now()

    def is_leave(self):
        return self.date_of_departure and self.date_of_departure < datetime.datetime.now()

    privileges_in_str.short_description = "Льготные категории"
    is_dead.short_description = "Умерший"
    is_leave.short_description = "Покинувший отделение"

    def get_absolute_url(self):
        return reverse('serviced_person_detail', args=[str(self.id)])

    def __str__(self):
        return self.FIO()


class Privilege(models.Model):
    class Meta:
        verbose_name = "Льготная категория"
        verbose_name_plural = "Льготные категории"

    title = models.TextField(max_length=1024, verbose_name="Название категории")

    def __str__(self):
        return self.title


# Keep minimal needed info from passport to perform data in documents
class PassportData(models.Model):
    class Meta:
        verbose_name = "Пасспортные данные"
        verbose_name_plural = "Пасспортные данные"

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
