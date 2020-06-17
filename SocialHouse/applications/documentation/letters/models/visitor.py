import datetime

from django.db import models

from applications.department.people.models import Visitor
from .abstract import LetterBase


class LetterVisitor(LetterBase):
    class Meta:
        verbose_name = "Заявление на предоставление гостевой визы"
        verbose_name_plural = "Заявления на предоставление гостевой визы"

    __template_name__ = "visitor.docx"

    visitor = models.ForeignKey(to=Visitor, verbose_name="Посетитель", on_delete=models.CASCADE, )
    date_to = models.DateField(verbose_name="Дата прекращения действия заявления",
                               help_text="Конечный срок гостевой визы", default=datetime.datetime.now)
    commentary = models.TextField(verbose_name="Комментарий", max_length=4096, blank=True, null=True,
                                  help_text="Не будет отражен в документе", )
