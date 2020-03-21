from django.db import models

# Create your models here.
from .enums import StatementEnum


class Statement(models.Model):
    class Meta:
        verbose_name = "Условие для услуги"
        verbose_name_plural = "Условия для услуг"

    statement = models.CharField(verbose_name="Логический оператор", max_length=2,
                                 choices=StatementEnum.choices, default=StatementEnum.EQUAL)
    limit = models.FloatField(verbose_name="Ограничение", default=1)

    def check_limit(self, num: float) -> bool:
        if self.statement == StatementEnum.LESS_EQUAL:
            return num <= self.limit
        if self.statement == StatementEnum.EQUAL:
            return num == self.limit
        # Undefined
        raise Exception("Не указано условие")

    def get_diff(self, num: float) -> float:
        return num - self.limit

    def __str__(self):
        return f"{self.get_statement_display()} {self.limit}"


def default_statement():
    statement = Statement.objects.get_or_create(
        statement=StatementEnum.EQUAL,
        limit=1.0
    )[0]
    statement.save()
    return statement.id
