from django.db.models import TextChoices


class MeterTypesEnum(TextChoices):
    WATER_COLD = 'C', "Холодная вода"
    WATER_WARM = 'W', "Горячая вода"
    GASOLINE = 'G', "Газосноснабжение"
    ELECTRICITY = 'E', "Электричество"
    HEATING = 'O', "Отопление"
