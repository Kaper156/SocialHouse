from django.db.models.signals import pre_save
from django.dispatch import receiver

from applications.social_work.ippsu.exceptions import ServiceNotIncluded
from applications.social_work.providing.models import ProvidedService
from utils.clone import clone, force_save


@receiver(pre_save, sender=ProvidedService)
def check_provided_service(sender, instance: ProvidedService, **kwargs):
    default_clones = list()  # Clones of inst which have max limit and q=1
    other_clones = list()  # Clones with remain volume (and for G, clones which have type PfG)

    # Check including
    if instance.is_from_guaranteed():
        # Is Guaranteed
        if instance.service not in instance.journal.ippsu.included_services.all():
            # If service.type is Guranteed, then it must be in ippsu.included_services
            raise ServiceNotIncluded()

    # Split by q and volume
    update_dict = {'quantity': 1}
    volume_limit = instance.service.volume_limitation.limit
    if instance.volume > volume_limit:
        # Calculate count of copy which have maximum volume multiplied by quantity (because q must be 1)
        count_of_full_volume_copy = int(instance.volume // volume_limit) * instance.quantity
        # Set max volume to copies
        update_dict['volume'] = volume_limit
        # Add clones with max volume
        default_clones.extend(clone(instance, sender, count=count_of_full_volume_copy, update_dict=update_dict))

        # Calculate remain volume
        remain_volume = instance.volume - (count_of_full_volume_copy * volume_limit)
        if remain_volume > 0:
            # if instance have remain volume
            update_dict['volume'] = remain_volume
            other_clones.extend(clone(instance, sender, 1, update_dict=update_dict))
        instance.volume = volume_limit
        instance.quantity = 1
    else:
        default_clones.extend(clone(instance, sender, count=instance.quantity, update_dict=update_dict))
        instance.quantity = 1

    # Switch first clone and self
    # instance = default_clones[0]
    del default_clones[0]
    force_save(ProvidedService, other_clones)
    force_save(ProvidedService, default_clones)
    return instance
