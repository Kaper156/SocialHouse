import datetime

from django.db import models

from applications.department.people.models import ServicedPerson
from ...standardization.models import DocumentDocx


class LetterBase(DocumentDocx):
    class Meta:
        abstract = True

    date_of_application = models.DateField(verbose_name="Дата подачи заявления", default=datetime.datetime.now)
    date_from = models.DateField(verbose_name="Дата начала действия заявления", default=datetime.datetime.now,
                                 help_text="Установите дату с которой заявление будет действовать "
                                           "(например дата с которой прекратится оказание платных услуг)")
    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.CASCADE, related_name='%(class)s',
                                        # limit_choices_to= # TODO: Maybe set active?
                                        verbose_name="Обслуживаемый"
                                        )

    def template_name(self):
        return "letter.docx"
