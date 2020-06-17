import datetime

from django.db import models

from ..general_data.models import DepartmentInfo, default_department
from ..people.models import Visitor


class Event(models.Model):
    # TODO maybe change to proxy-table
    class Meta:
        verbose_name = "Событие в отделении"
        verbose_name_plural = "События в отделении"

    department_info = models.ForeignKey(to=DepartmentInfo, on_delete=models.PROTECT, related_name='events',
                                        verbose_name="Информация об отделении", default=default_department)
    title = models.CharField(max_length=1024, verbose_name="Название")
    description = models.TextField(verbose_name="Описание события",
                                   help_text="Будет использовано для ежегодного отчёта")
    date_of = models.DateField(verbose_name="Дата", default=datetime.datetime.now)
    visitors = models.ManyToManyField(to=Visitor, related_name="events", verbose_name="Участвующие посетители")
    commentary = models.TextField(verbose_name="Комментарий", help_text="Не отображается в документации и новостях")
