from django.contrib import admin

from .models import ServiceMeasurement, ServicesList, Service


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
