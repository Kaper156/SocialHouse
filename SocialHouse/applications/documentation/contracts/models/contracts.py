import os

from django.core.exceptions import ValidationError
from django.db import models

from .abstract import ContractBase
from ..enums import ContractTypeEnum


class Contract(ContractBase):
    class Meta:
        abstract = True

    # TODO make signal - after set archieved
    date_expiration = models.DateField(verbose_name="Прекратил действие", editable=False, default=None, null=True)

    def clean(self):
        if self.date_expiration and self.date_from > self.date_expiration:
            raise ValidationError(f"Договор не может быть прекращен, раньше чем был начат "
                                  f"(от {self.date_from} до {self.date_expiration})")


# TODO another template
class SocialContract(Contract):
    class Meta:
        verbose_name = "Договор на оказание социальных услуг"
        verbose_name_plural = "Договоры на оказание социальных услуг"

    __template_name__ = "ippsu.docx"  # TODO: change
    __files_dir__ = os.path.join('contracts', 'social')

    contract_type = ContractTypeEnum.SOCIAL


class PaidContract(Contract):
    class Meta:
        verbose_name = "Договор на оказание платных услуг"
        verbose_name_plural = "Договоры на оказание платных услуг"

    __template_name__ = "ippsu.docx"  # TODO: change
    __files_dir__ = os.path.join('contracts', 'paid')

    contract_type = ContractTypeEnum.PAID
