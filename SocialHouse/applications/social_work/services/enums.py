from django.db.models.enums import TextChoices


class ServiceTypeEnum(TextChoices):
    GUARANTEED = 'G', "гарантированная"
    ADDITIONAL = 'A', "дополнительная"
    PAID = 'P', "платная"
    CALCULATING = 'C', "-вычисляется-"


