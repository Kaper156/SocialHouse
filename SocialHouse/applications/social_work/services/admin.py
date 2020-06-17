from django.contrib import admin

from .models import ServiceMeasurement, ServicesList, Service


@admin.register(ServiceMeasurement)
class ServiceMeasurementAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


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
        # 'services_list',
        # 'place',
        'volume_limitation',
        'period_limitation',
    )
    list_filter = ('services_list', 'type_of_service', 'service_category',)
    sortable_by = ('type_of_service', 'title', 'measurement', 'time_for_service', 'volume_limitation',
                   'period_limitation',),
    search_fields = ('title', 'measurement')
