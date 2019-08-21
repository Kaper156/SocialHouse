from django.db import models
from django.contrib.auth.models import User, Group

import datetime

# TODO show hint about format (dd.mm.yyyy) in all "date_of_birth" fields

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
        ('ME', "Больничный"),
        ('VA', "В отпуске"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    name = models.CharField(max_length=128, blank=True, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=256, blank=True, verbose_name="Фамилия")

    gender = models.CharField(default='F', choices=GENDERS, max_length=1, verbose_name="Пол")
    # TODO forms: http://qaru.site/questions/107195/django-booleanfield-as-radio-buttons
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    status = models.CharField(max_length=2, choices=STATUSES, verbose_name="Статус", default='WO')

    # positions = models.ManyToManyField('Position', through='WorkerPosition', related_name='Workers')

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

    # TODO переделать описание
    # TODO default LI
    # TODO if status de - show when
    STATUSES = (
        ('LI', "Жив"),
        ('DE', "Мертв"),
        ('ME', "На лечении"),
        ('OU', "В поездке"),
        ('LE', "Выписан"),
    )
    name = models.CharField(max_length=128, verbose_name="Имя")
    patronymic = models.CharField(max_length=128, blank=True, verbose_name="Отчество")
    surname = models.CharField(max_length=256, verbose_name="Фамилия")

    gender = models.CharField(default='F', choices=GENDERS, max_length=1, verbose_name="Пол")
    date_of_birth = models.DateField(null=True, verbose_name="Дата рождения")
    status = models.CharField(choices=STATUSES, max_length=2, verbose_name="Статус")
    date_of_death = models.DateField(null=True, blank=True, verbose_name="Дата смерти")

    def FIO(self, full=False):
        if not full:
            return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"
        return f"{self.name} {self.patronymic} {self.surname}"

    def __str__(self):
        return self.FIO()
