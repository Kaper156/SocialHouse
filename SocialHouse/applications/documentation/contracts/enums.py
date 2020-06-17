from django.db.models.enums import TextChoices


class ContractStatusEnum(TextChoices):
    ACTIVE = 'A', "действителен"
    PAUSE = 'P', "приостановлен"
    DISABLED = 'D', "не действителен"


class ContractReasonsEnum(TextChoices):
    ACTIVE = 'A', "возобновить"
    PAUSE = 'P', "приостановить"
    DISABLE = 'D', "прекратить"


class ContractTypeEnum(TextChoices):
    IPPSU = 'I', "ИППСУ"
    SOCIAL = 'S', "Договор на оказание социальных услуг"
    PAID = 'P', "Договор на оказание платных услуг"
