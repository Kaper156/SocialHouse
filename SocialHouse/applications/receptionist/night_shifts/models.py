import datetime

from django.contrib.auth.models import User
from django.db import models

from applications.department.people.models import ServicedPerson, WorkerPosition, Visitor


class NightShift(models.Model):
    class Meta:
        verbose_name = "Ночная смена"
        verbose_name_plural = "Ночные смены"

    receptionist = models.ForeignKey(verbose_name="Ответственный администратор", to=WorkerPosition,
                                     on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата", default=datetime.datetime.now, unique=True)

    @staticmethod
    def get_or_create_by_position(position: WorkerPosition):
        now = datetime.datetime.now().date()
        shift = None
        if NightShift.objects.filter(date=now).count():
            shift = NightShift.objects.get(date=now)
        return shift or NightShift.objects.get_or_create(
            date=now,
            receptionist=position
        )[0]

    def __str__(self):
        return f"{self.receptionist.worker.FIO(False)} ({self.date})"


class ServicedPersonOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении обслуживаемый"
        verbose_name_plural = "Ночующие в отделении обслуживаемые"

    overnight = models.ForeignKey(verbose_name="Ночь", to=NightShift, on_delete=models.CASCADE)
    serviced_person = models.ForeignKey(verbose_name="Обслуживаемый", to=ServicedPerson, on_delete=models.CASCADE)


# TODO
class ServicedShiftEvent(models.Model):
    class Meta:
        verbose_name = "Событие с обслуживаемым"
        verbose_name_plural = "События с обслуживаемыми"

    date_of = models.DateTimeField(default=datetime.datetime.now)
    serviced_overnight = models.ForeignKey(to=ServicedPersonOvernight, on_delete=models.CASCADE)
    commentary = models.TextField()


class VisitorOvernight(models.Model):
    class Meta:
        verbose_name = "Ночующий в отделении посетитель"
        verbose_name_plural = "Ночующие в отделении посетители"

    overnight = models.ForeignKey(verbose_name="Ночь", to=NightShift, on_delete=models.CASCADE)
    visitor = models.ForeignKey(verbose_name="Посетитель", to=Visitor, on_delete=models.CASCADE)
    # Todo rename field to visitor


# TODO
class VisitorShiftEvent(models.Model):
    class Meta:
        verbose_name = "Событие с посетителем"
        verbose_name_plural = "События с посетителями"

    date_of = models.DateTimeField(default=datetime.datetime.now)
    visitor_overnight = models.ForeignKey(to=VisitorOvernight, on_delete=models.CASCADE)
    commentary = models.TextField()
