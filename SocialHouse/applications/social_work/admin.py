from django.contrib import admin

from .models import ServiceMeasurement, ServicesList, Service, IPPSU, IncludedService, ProvidedService


@admin.register(ServiceMeasurement)
class ServiceMeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'statement', 'count', 'period')


@admin.register(ServicesList)
class ServicesListAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_from', 'date_to', 'is_archived')
    list_filter = ('date_from', 'date_to', 'is_archived')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'type_of_service',
        'service_category',
        'measurement',
        'tax',
        'time_for_service',
        'services_list',
        'place',
    )
    raw_id_fields = ('measurement', 'services_list')


@admin.register(IPPSU)
class IPPSUAdmin(admin.ModelAdmin):
    list_display = (
        'social_worker',
        'serviced_person',
        'date_from',
        'date_to',
        'is_archived',
    )
    date_hierarchy = 'date_from'
    list_filter = (
        'social_worker',
        'serviced_person',
        'date_from',
        'date_to',
        'is_archived',
    )


@admin.register(IncludedService)
class IncludedServiceAdmin(admin.ModelAdmin):
    list_display = ('IPPSU', 'service')
    list_filter = ('IPPSU', 'service')


@admin.register(ProvidedService)
class ProvidedServiceAdmin(admin.ModelAdmin):
    list_display = ('ippsu', 'date_of', 'service', 'type_of_service')
    list_filter = (
    'ippsu', 'date_of', 'service__type_of_service', 'ippsu__serviced_person', 'service__service_category')
    # date_hierarchy = 'date_of',
    # filter_horizontal = ('service',)
    # search_fields = ('service__title',)
