from django.db import models

from .abstract import LetterBase
from ...contracts.enums import ContractTypeEnum, ContractReasonsEnum

LETTER_CONTRACT_TEMPLATE_NAMES = {
    ContractTypeEnum.SOCIAL.value: {
        ContractReasonsEnum.PAUSE.value: "social_pause.docx",
        ContractReasonsEnum.ACTIVE.value: "social_.docx",
        ContractReasonsEnum.DISABLE.value: "social_.docx",
    },
    ContractTypeEnum.PAID.value: {
        ContractReasonsEnum.PAUSE.value: "paid_pause.docx",
        ContractReasonsEnum.ACTIVE.value: "paid_active.docx",
        ContractReasonsEnum.DISABLE.value: "paid_disable.docx",
    },
    ContractTypeEnum.IPPSU.value: {
        ContractReasonsEnum.PAUSE.value: "ippsu_pause.docx",
        ContractReasonsEnum.ACTIVE.value: "ippsu_active.docx",
        ContractReasonsEnum.DISABLE.value: "ippsu_disable.docx",
    }
}


class LetterContract(LetterBase):
    class Meta:
        verbose_name = "Заявление (договоры/ИППСУ)"
        verbose_name_plural = "Заявления (договоры/ИППСУ)"

    contract_type = models.CharField(verbose_name="Вид договора", choices=ContractTypeEnum.choices,
                                     max_length=1, default=ContractTypeEnum.SOCIAL, editable=True)

    reason = models.CharField(verbose_name="Цель заявления", choices=ContractReasonsEnum.choices,
                              max_length=1, default=ContractReasonsEnum.PAUSE, editable=True)

    def template_name(self):
        return LETTER_CONTRACT_TEMPLATE_NAMES[self.contract_type][self.reason]
