from django.db.models.enums import TextChoices, IntegerChoices


class PeriodEnum(IntegerChoices):
    DAY = 1, "день"
    WEEK = 7, "неделя"
    MONTH = 31, "месяц"
    __empty__ = "-Неопределенно-"


class StatementEnum(TextChoices):
    LESS_EQUAL = 'le', "менее/до/не более (включая) (<=)"
    EQUAL = 'eq', "ровно (==)"
