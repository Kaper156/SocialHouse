from django.db.models.enums import TextChoices


class ServiceTypeEnum(TextChoices):
    GUARANTEED = 'G', "гарантированная"
    ADDITIONAL = 'A', "дополнительная"
    PAID = 'P', "платная"
    CALCULATING = 'C', "-вычисляется-"


class WorkerPositionEnum(TextChoices):
    CHIEF = 'C', "Заведующий отделением"
    SOCIAL_WORKER = 'S', "Социальный работник"
    NURSE = 'N', "Сиделка"
    RECEPTIONIST = 'R', "Администратор отделения"
