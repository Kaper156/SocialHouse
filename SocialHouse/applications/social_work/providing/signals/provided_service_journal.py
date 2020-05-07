from django.db.models.signals import pre_save
from django.dispatch import receiver

from applications.social_work.limitations.enums import PeriodEnum
from applications.social_work.limitations.utils.datetime import range_by_period_name
from applications.social_work.services.enums import ServiceTypeEnum
from ..models import ProvidedServiceJournal, ProvidedService


@receiver(pre_save, sender=ProvidedServiceJournal)
def check_provided_service(sender, instance: ProvidedServiceJournal, **kwargs):
    guaranteed_services = instance.services.filter(service__type_of_service=ServiceTypeEnum.GUARANTEED)
    # Get only with period limitations
    guaranteed_services = guaranteed_services.exclude(service__period_limitation__isnull=True)
    if not guaranteed_services.exists():
        return

    while guaranteed_services.exists():
        current_provided_service = guaranteed_services.first()
        # current_provided_service = ProvidedService()
        current_service = current_provided_service.service

        period_range = range_by_period_name(current_service.period_limitation.period, current_provided_service.date_of)
        neighbors_by_period = guaranteed_services.filter(
            service=current_service,
            date_of__range=period_range,
            # date_of__gt=period_range[0],
            # date_of__lt=period_range[1],
        )

        # For week range
        # if current journal start not from Monday, old provided services must be taken into neigbors_by_period

        if current_service.period_limitation.period == PeriodEnum.WEEK \
                and period_range[0].date() < current_provided_service.journal.date_from:
            provided_before = ProvidedService.objects.filter(
                journal__ippsu=instance.ippsu,
                service__type_of_service=ServiceTypeEnum.GUARANTEED,
                service=current_provided_service.service,
                date_of__lt=instance.date_from,
                date_of__gt=period_range[0]
            )
            neighbors_by_period = neighbors_by_period.union(provided_before)

        for cur_quantity, provided_service in enumerate(neighbors_by_period.all()):
            if cur_quantity >= current_service.period_limitation.limit:
                # Greater or equal because we start enumerate from 0
                provided_service.type_of_service = ServiceTypeEnum.PAID_FROM_GUARANTEED
            else:
                provided_service.type_of_service = ServiceTypeEnum.GUARANTEED
            provided_service.save()

        guaranteed_services = guaranteed_services.exclude(id__in=neighbors_by_period.values('id'))
