import datetime

from django.db import models

from ..enums import WorkerPositionEnum


class WorkerPositionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(dismissal_date__isnull=True, date_of_appointment__lte=datetime.datetime.now())

    def social_workers(self):
        return self.filter(position=WorkerPositionEnum.SOCIAL_WORKER)

    def chiefs(self):
        return self.filter(position=WorkerPositionEnum.CHIEF)

    def receptionists(self):
        return self.filter(position=WorkerPositionEnum.RECEPTIONIST)


class WorkerPositionManager(models.Manager):
    def get_queryset(self):
        return WorkerPositionQuerySet(self.model)
