from django.contrib import admin

from .forms import IncludedServiceForm
from .models import ServiceMeasurement, ServicesList, Service, IPPSU, IncludedService, ProvidedService, \
    ProvidedServiceJournal, Statement


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('statement', 'limit')


@admin.register(ServiceMeasurement)
class ServiceMeasurementAdmin(admin.ModelAdmin):
    list_display = ('title', 'period_statement', 'period', 'volume_statement')


@admin.register(ServicesList)
class ServicesListAdmin(admin.ModelAdmin):
    list_display = ('date_from', 'date_to', 'is_archived')
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
    # raw_id_fields = ('measurement', 'services_list')



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
    form = IncludedServiceForm
    list_display = ('IPPSU', 'service')
    list_filter = ('IPPSU', 'service')


@admin.register(ProvidedService)
class ProvidedServiceAdmin(admin.ModelAdmin):
    list_display = ('journal', 'date_of', 'service', 'type_of_service')
    list_filter = ('journal', 'date_of', 'service__type_of_service',
                   'journal__ippsu__serviced_person', 'service__service_category')
    # date_hierarchy = 'date_of',
    # filter_horizontal = ('service',)
    # search_fields = ('service__title',)


@admin.register(ProvidedServiceJournal)
class ProvidedServiceJournalAdmin(admin.ModelAdmin):
    list_display = ('ippsu', 'period', 'date_from', 'date_to')
    sortable_by = ('period', 'date_from', 'date_to')
    list_filter = ('ippsu__serviced_person', 'ippsu__social_worker__worker')
    date_hierarchy = 'date_from'
