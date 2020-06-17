from django.db.models.signals import pre_save
from django.dispatch import receiver

from applications.documentation.standardization.signals import document_pre_save
from .models import SocialAct, PaidAct


@receiver(pre_save, sender=SocialAct)
def set_total_social_act(sender, instance, **kwargs):
    instance.set_totals()


@receiver(pre_save, sender=PaidAct)
def set_total_paid_act(sender, instance, **kwargs):
    instance.set_totals()


pre_save.connect(document_pre_save, sender=SocialAct)
pre_save.connect(document_pre_save, sender=PaidAct)
