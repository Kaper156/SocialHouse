import datetime

from django.db import models

from applications.department.people.models import WorkerPosition, ServicedPerson, WorkerPositionEnum
from ..enums import ContractStatusEnum, ContractTypeEnum
from ...standardization.models import DocumentDocx


class ContractBase(DocumentDocx):
    class Meta:
        abstract = True

    # TODO form with limit choice not null dismiss
    executor = models.ForeignKey(to=WorkerPosition, on_delete=models.DO_NOTHING, related_name="%(class)s",
                                 verbose_name="Исполнитель услуг",
                                 limit_choices_to={'position': WorkerPositionEnum.SOCIAL_WORKER, })
    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.CASCADE, related_name="%(class)s",
                                        verbose_name="Обслуживаемый")
    serial_number = models.CharField(verbose_name="Номер договора", help_text="знак № будет подставлен автоматически",
                                     max_length=128)
    date_from = models.DateField(verbose_name="Действует от", default=datetime.datetime.now)
    contract_status = models.CharField(verbose_name="Статус", choices=ContractStatusEnum.choices,
                                       max_length=1, default=ContractStatusEnum.ACTIVE, editable=False)

    is_archived = models.BooleanField(verbose_name="В архиве",
                                      help_text="Для совместимости со старыми отчетами, "
                                                "установите данный флаг, вместо удаления",
                                      default=False)
    contract_type = ContractTypeEnum  # Make None?

    def __str__(self):
        return f"{self.serviced_person} от {self.date_from} №{self.serial_number} (Исп.: {self.executor})"
