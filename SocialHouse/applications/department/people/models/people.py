import datetime

from django.contrib.auth.models import User
from django.db import models

from .abstract import ExtendedPerson
from ..enums import WorkerPositionEnum
from ..querysets import WorkerPositionManager
from ...general_data.models import DepartmentInfo


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

    def positions(self):
        return '; '.join(wp.get_position_display() for wp in self.membership.all())

    positions.short_description = "Занимаемые должности"

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Worker.objects.get(user=self.user)
                self.pk = p.pk
            except Worker.DoesNotExist:
                pass

        super(Worker, self).save(*args, **kwargs)


class PositionActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(dismissal_date__isnull=True,
                                             date_of_appointment__lte=datetime.datetime.now())


def position_short(position):
    position = WorkerPositionEnum(position)
    if position == WorkerPositionEnum.CHIEF:
        return "Зав"
    elif position == WorkerPositionEnum.RECEPTIONIST:
        return "Адм"
    elif position == WorkerPositionEnum.SOCIAL_WORKER:
        return "Соц"


class WorkerPosition(models.Model):
    class Meta:
        verbose_name = "Ставка сотрудника"
        verbose_name_plural = "Ставки сотрудников"
        base_manager_name = 'objects'

    worker = models.ForeignKey('Worker', related_name='membership', on_delete=models.CASCADE, verbose_name="Сотрудник")
    position = models.CharField(verbose_name="Должность", max_length=1,
                                choices=WorkerPositionEnum.choices, default=WorkerPositionEnum.SOCIAL_WORKER)
    date_of_appointment = models.DateField(verbose_name="Дата устройства на должность",
                                           default=datetime.datetime.now)
    dismissal_date = models.DateField(verbose_name="Дата увольнения с должности", null=True, blank=True)
    rate = models.FloatField(verbose_name="Ставка", default=1)
    department = models.ForeignKey(to=DepartmentInfo, on_delete=models.PROTECT, related_name='workers',
                                   limit_choices_to={'is_archived': False})
    # objects = models.Manager()
    objects = WorkerPositionManager()

    def __str__(self):
        if self.rate != 1:
            # return f'{self.worker.FIO(full=False)} ({self.get_position_display()}) [x{self.rate}]'
            return f'[{position_short(self.position)}(x{self.rate})] {self.worker.FIO(full=False)}'
        return f'[{position_short(self.position)}] {self.worker.FIO(full=False)}'

    def get_active_IPPSU_set(self):
        now = datetime.datetime.now().date()
        return self.ippsu.filter(is_archived=False, date_expiration__gte=now)

    def try_start_night_shift(self):
        from applications.receptionist.night_shifts.models import NightShift
        shift = NightShift.get_or_create_by_position(self)
        print(shift)
        return shift  # , shift.receptionist.id == self.id


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

    # privileges = models.ManyToManyField(to=Privilege, verbose_name='Льготные категории', blank=True)
    spouse = models.ForeignKey(to="self", on_delete=models.SET_NULL, related_name='+', null=True, default=None,
                               verbose_name="Супруг(а)")
    date_of_income = models.DateField(null=True, blank=True, verbose_name="Дата прибытия")
    # TODO make hidden on creation
    date_of_death = models.DateField(null=True, blank=True, verbose_name="Дата смерти")
    date_of_departure = models.DateField(null=True, blank=True, verbose_name="Дата ухода")

    # TODO signal with RoomChangeLetter
    room = models.IntegerField(verbose_name="Номер комнаты", editable=False)
    floor = models.IntegerField(verbose_name="Этаж", editable=False)

    #
    # passport_data = models.OneToOneField(to=PassportData, on_delete=models.CASCADE,
    #                                      verbose_name="Пасспортные данные", related_name='serviced_person')

    def privileges_in_str(self):
        if not self.privileges.exists():
            return 'Без льгот'
        return '; '.join(p.privilege.title for p in self.privileges.all())

    def is_dead(self):
        return self.date_of_death and self.date_of_death < datetime.datetime.now()

    def is_leave(self):
        return self.date_of_departure and self.date_of_departure < datetime.datetime.now()

    def age_category(self):
        date_diff = datetime.datetime.now().date() - self.date_of_birth
        year_diff = date_diff.days // 365
        if self.gender == "M":
            if year_diff <= 59:
                return "18-59"
            elif year_diff <= 74:
                return "60-74"
            elif year_diff <= 79:
                return "75-79"
            elif year_diff <= 89:
                return "80-89"
            else:
                return "Старше 90"
        else:
            if year_diff <= 54:
                return "18-54"
            if year_diff <= 59:
                return "55-59"
            elif year_diff <= 74:
                return "60-74"
            elif year_diff <= 79:
                return "75-79"
            elif year_diff <= 89:
                return "80-89"
            else:
                return "Старше 90"

    def address_in_department(self):
        return f"{self.room} ({self.floor})"

    address_in_department.short_description = "Комната"
    age_category.short_description = "Возрастная категория"
    privileges_in_str.short_description = "Льготные категории"
    is_dead.short_description = "Умерший"
    is_leave.short_description = "Покинувший отделение"

    # def get_absolute_url(self):
    #     return reverse('serviced_person_detail', args=[str(self.id)])

    def get_active_IPPSU_set(self):
        now = datetime.datetime.now().date()
        return self.ippsu  # .filter(is_archived=False)#, date_expiration__gte=now)

    def __str__(self):
        return self.FIO()


class Visitor(ExtendedPerson):
    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

    commentary = models.TextField(verbose_name="Комментарий", max_length=2048, blank=True)
