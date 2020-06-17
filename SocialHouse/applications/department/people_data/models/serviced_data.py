from django.db import models

from applications.department.people.models import ServicedPerson


class PassportData(models.Model):
    class Meta:
        verbose_name = "Пасспортные данные"
        verbose_name_plural = "Пасспортные данные"

    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.PROTECT,
                                        verbose_name="Обслуживаемый", related_name='passport_data')
    # Not confidential!
    # serial = models.CharField(max_length=4, verbose_name="Серия")
    # number = models.CharField(max_length=6, verbose_name="Номер")
    # date_of_issue = models.DateField(verbose_name="Дата выдачи")
    issued_authority = models.TextField(verbose_name="Выдан органом")
    is_archived = models.BooleanField(verbose_name="В архиве", default=False)

    def __str__(self):
        if self.serviced_person.gender == 'M':
            return f"Пасспорт гр-на {self.serviced_person}"
        else:
            return f"Пасспорт гр-ки {self.serviced_person}"


class Privilege(models.Model):
    class Meta:
        verbose_name = "Льготная категория"
        verbose_name_plural = "Льготные категории"

    title = models.TextField(max_length=1024, verbose_name="Название категории")

    def __str__(self):
        return self.title


class PrivilegeCertificate(models.Model):
    class Meta:
        verbose_name = "Удостоверение льготной категории"
        verbose_name_plural = "Удостоверения льготных категорий"

    serviced_person = models.ForeignKey(to=ServicedPerson, on_delete=models.PROTECT, related_name='privileges',
                                        verbose_name="Обслуживаемый")
    privilege = models.ForeignKey(to=Privilege, on_delete=models.PROTECT, related_name='certificates',
                                  verbose_name="Категория")
    date_of = models.DateField(verbose_name="Дата присвоения")


def default_privileges_for_additional():
    return Privilege.objects.all()
