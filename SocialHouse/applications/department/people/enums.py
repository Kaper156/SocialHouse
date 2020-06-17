from django.db.models import TextChoices


class WorkerPositionEnum(TextChoices):
    CHIEF = 'C', "Заведующий отделением"
    SOCIAL_WORKER = 'S', "Социальный работник"
    # NURSE = 'N', "Сиделка"
    RECEPTIONIST = 'R', "Администратор отделения"


class IncomeTypeEnum(TextChoices):
    ANOTHER_DEPARTMENT = 'A', "Из другого отделения"
    CONTRACT_FIRST_TIME = 'C', "Заключен первичный договор"
