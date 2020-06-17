import datetime

from django.db import models


class DepartmentInfo(models.Model):
    class Meta:
        verbose_name = 'Отделение соцального обслуживания'
        verbose_name_plural = 'Отделения соцального обслуживания'

    department_title = models.TextField(verbose_name="Полное наименование отделения")
    department_title_short = models.TextField(verbose_name="Сокращенное наименование отделения", max_length=1024)

    department_address = models.TextField(verbose_name="Полный адрес отделения", )
    department_address_region = models.CharField(max_length=1024, verbose_name="Район")
    department_address_city = models.CharField(max_length=1024, verbose_name="Населенный пункт")
    department_address_street = models.CharField(max_length=1024, verbose_name="Улица")
    department_address_house = models.CharField(max_length=1024, verbose_name="Дом")

    department_rooms = models.PositiveIntegerField(verbose_name="Количество комнат")
    department_floors = models.PositiveIntegerField(verbose_name="Количество этажей")

    department_type = "на дому"
    department_phone_number = models.CharField(verbose_name="Номер телефона", max_length=15)

    kcson_chief = models.CharField(verbose_name="Фамилия имя и отчество заведующего КЦСОН",
                                   max_length=256, blank=False, null=False)
    kcson_chief_short = models.CharField(verbose_name="ФИО заведующего КЦСОН (инициалы)",
                                         max_length=256, blank=False, null=False)
    kcson_title = models.TextField(verbose_name="Полное наименование КЦСОН", max_length=2048)
    kcson_title_short = models.TextField(verbose_name="Сокращенное наименование КЦСОН", max_length=1024)

    date_of_create = models.DateTimeField(verbose_name="Дата внесения информации", default=datetime.datetime.now)
    # TODO make all other archieved after add new data
    is_archived = models.BooleanField(verbose_name="В архиве", default=False)

    def get_department_chief(self):
        from ..people.enums import WorkerPositionEnum
        return self.workers.filter(position=WorkerPositionEnum.CHIEF, dismissal_date=None).first()

    get_department_chief.description = "Заведующий отделением"

    # TODO make all other archived
    # def clean(self):
    #     pass

    def __str__(self):
        return f"{self.get_department_chief()} / {self.kcson_chief} ({self.date_of_create})"


def default_department():
    # Warning: can be used only after set minimum one depInfo
    return DepartmentInfo.objects.filter(is_archived=False).order_by('date_of_create').first()
