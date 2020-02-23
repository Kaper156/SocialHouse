import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Travel, SickLeave
from applications.core.models import ServicedPerson


# Todo: check status, before save
# normal_status = ServicedPerson.STATUSES[0][0]

def check_dates(instance):
    date_now = datetime.datetime.now().date()
    if instance.date_from <= date_now:
        if (instance.date_to and instance.date_to > date_now) or not instance.date_to:
            print(f"Date correct for {instance}")
            return True
    return False


@receiver(pre_save, sender=Travel)
def travel_save_handler(sender, instance, **kwargs):
    new_status = ServicedPerson.STATUSES[2][0]

    if check_dates(instance):
        instance.serviced_person.location = new_status
        instance.serviced_person.save()


@receiver(pre_save, sender=SickLeave)
def travel_save_handler(sender, instance, **kwargs):
    status = ServicedPerson.STATUSES[1][0]
    if check_dates(instance):
        instance.serviced_person.location = status
        instance.serviced_person.save()
