from django.db.models import TextChoices


class WorkerPositionEnum(TextChoices):
    CHIEF = 'C', "Заведующий отделением"
    SOCIAL_WORKER = 'S', "Социальный работник"
    NURSE = 'N', "Сиделка"
    RECEPTIONIST = 'R', "Администратор отделения"
