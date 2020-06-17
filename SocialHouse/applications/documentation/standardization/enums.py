from django.db.models import TextChoices


class DocumentPeriodTypeEnum(TextChoices):
    MONTH = 'M', "месяц"
    QUARTER = 'Q', "квартал"
    YEAR = 'Y', "год"
