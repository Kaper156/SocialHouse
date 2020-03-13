import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from applications.core.enums import WorkerPositionEnum
from applications.core.models.abstract import ExtendedPerson


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
        return '; '.join(wp.position.description for wp in self.membership.all())

    get_positions.short_description = "Занимаемые должности"

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Worker.objects.get(user=self.user)
                self.pk = p.pk
            except Worker.DoesNotExist:
                pass

        super(Worker, self).save(*args, **kwargs)


class WorkerPosition(models.Model):
    class Meta:
        verbose_name = "Ставка сотрудника"
        verbose_name_plural = "Ставки сотрудников"

    worker = models.ForeignKey('Worker', related_name='membership', on_delete=models.CASCADE, verbose_name="Сотрудник")
    position = models.CharField(verbose_name="Должность", max_length=1,
                                choices=WorkerPositionEnum.choices, default=WorkerPositionEnum.SOCIAL_WORKER)
    date_of_appointment = models.DateField(verbose_name="Дата устройства на должность",
                                           default=datetime.datetime.now)
    dismissal_date = models.DateField(verbose_name="Дата увольнения с должности", null=True, blank=True)
    rate = models.FloatField(verbose_name="Ставка", default=1)

    def __str__(self):
        if self.rate != 1:
            return f'{self.worker.FIO(full=False)} ({self.get_position_display()}) [x{self.rate}]'
        return f'{self.worker.FIO(full=False)} ({self.get_position_display()})'


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

    contract_number = models.CharField(verbose_name="Номер договора", max_length=128,
                                       blank=False, null=False, default="№ ")
    date_of_income = models.DateField(verbose_name="Дата заключения договора", default=datetime.datetime.now)

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
