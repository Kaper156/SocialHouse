# from django.db import models
#
#
# class WorkerPositionQuerySet(models.QuerySet):
#     def active(self):
#         return self.filter(position=)
#
#     def social_workers(self):
#         return self.filter(width__lte=models.F('height'))
#
#     def chiefs(self):
#         return self.filter(width__lte=1200)
#
#     def receptionists(self):
#         return self.filter(width__gte=1200)
#
#
# class WorkerPositionManager(models.Manager):
#     def get_queryset(self):
#         return WorkerPositionQuerySet(self.model)
